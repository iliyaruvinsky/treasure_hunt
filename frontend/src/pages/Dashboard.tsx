import React, { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getFindings, getAnalysisRuns, getKpiSummary } from '../services/api';
import FocusAreaChart from '../components/charts/FocusAreaChart';
import RiskLevelChart from '../components/charts/RiskLevelChart';
import MoneyLossChart from '../components/charts/MoneyLossChart';
import FindingsTable from '../components/tables/FindingsTable';
import DashboardFilters, { FilterState } from '../components/filters/DashboardFilters';
import HelpTooltip from '../components/HelpTooltip';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FilterState>({
    focusArea: '',
    severity: '',
    status: '',
    dateFrom: '',
    dateTo: '',
  });

  const { data: kpiData, isLoading: isLoadingKpis, error: kpiError } = useQuery({
    queryKey: ['kpiSummary'],
    queryFn: getKpiSummary,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
  });

  const { data: findings, isLoading: isLoadingFindings, error: findingsError, refetch: refetchFindings } = useQuery({
    queryKey: ['findings', filters],
    queryFn: () =>
      getFindings({
        focus_area: filters.focusArea || undefined,
        severity: filters.severity || undefined,
        status: filters.status || undefined,
        date_from: filters.dateFrom || undefined,
        date_to: filters.dateTo || undefined,
      }),
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
    onError: (error) => {
      console.error('Failed to load findings:', error);
    },
  });

  const { data: analysisRuns, isLoading: runsLoading, error: runsError, refetch: refetchRuns } = useQuery({
    queryKey: ['analysisRuns'],
    queryFn: getAnalysisRuns,
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
    onError: (error) => {
      console.error('Failed to load analysis runs:', error);
    },
  });

  const latestRun = analysisRuns?.[0];

  // Debug logging
  useEffect(() => {
    if (findings) {
      console.log('Findings loaded:', findings.length);
      const withRisk = findings.filter(f => f.risk_assessment).length;
      const withMoney = findings.filter(f => f.money_loss_calculation).length;
      console.log('Findings with risk_assessment:', withRisk);
      console.log('Findings with money_loss_calculation:', withMoney);

      const totalRisk = findings.reduce((sum, f) => {
        const score = f.risk_assessment?.risk_score || 0;
        return sum + (typeof score === 'number' ? score : 0);
      }, 0);
      const totalMoney = findings.reduce((sum, f) => {
        const loss = f.money_loss_calculation?.estimated_loss || 0;
        return sum + (typeof loss === 'number' ? loss : 0);
      }, 0);
      console.log('Calculated Total Risk Score:', totalRisk);
      console.log('Calculated Total Money Loss:', totalMoney);
    }
  }, [findings]);

  // Totals from the new KPI endpoint
  const totalFindings = kpiData?.total_findings ?? 0;
  const totalRiskScore = kpiData?.total_risk_score ?? 0;
  const totalMoneyLoss = kpiData?.total_money_loss ?? 0;
  const totalAnalysisRuns = kpiData?.analysis_runs ?? 0;

  const numberFormatter = useMemo(
    () => new Intl.NumberFormat('en-US'),
    []
  );
  const currencyFormatter = useMemo(
    () =>
      new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
      }),
    []
  );

  // Aggregate data for charts - use findings data instead of just latest run
  const focusAreaData = findings?.reduce((acc: Record<string, number>, finding: any) => {
    const code = finding.focus_area?.code || 'UNKNOWN';
    acc[code] = (acc[code] || 0) + 1;
    return acc;
  }, {}) || latestRun?.findings_by_focus_area || {};
  const riskLevelData = findings?.reduce((acc: Record<string, number>, finding: any) => {
    const level = finding.risk_assessment?.risk_level || finding.severity || 'Unknown';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {}) || {};

  const moneyLossData = findings
    ?.map((f: any) => ({
      date: f.detected_at,
      amount: f.money_loss_calculation?.estimated_loss || 0,
    }))
    .filter((d: { amount: number }) => d.amount > 0)
    .sort((a: { date: string }, b: { date: string }) =>
      new Date(a.date).getTime() - new Date(b.date).getTime()
    ) || [];

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const handleFindingClick = (finding: any) => {
    navigate(`/findings/${finding.id}`);
  };

  if (isLoadingKpis || isLoadingFindings || runsLoading) {
    return (
      <div className="excavation-loader">
        <div className="scanner-line"></div>
        <div className="loading-text">
          <span className="glow">Loading Dashboard</span>
          <div className="loading-dots">
            <span style={{ animationDelay: '0s' }}>.</span>
            <span style={{ animationDelay: '0.2s' }}>.</span>
            <span style={{ animationDelay: '0.4s' }}>.</span>
          </div>
        </div>
      </div>
    );
  }

  if (kpiError || findingsError || runsError) {
    return (
      <div className="command-center">
        <div className="system-alert">
          <div className="alert-icon">⚠</div>
          <h2>Connection Error</h2>
          <p className="alert-detail">Unable to connect to the backend API</p>
          <p className="alert-endpoint">Expected: http://localhost:8080</p>
          <p className="alert-error">{kpiError?.message || findingsError?.message || runsError?.message || 'Unknown error'}</p>
          <button className="alert-retry" onClick={() => window.location.reload()}>
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="command-center">
      {/* Scan line effect */}
      <div className="scan-line"></div>

      {/* Header */}
      <header className="cc-header">
        <div className="header-left">
          <h1 className="cc-title">
            <span className="title-icon">◆</span>
            Treasure Hunt Analyzer
            <span className="title-sub">SAP Security & Compliance Insights</span>
          </h1>
        </div>
        <div className="header-right">
          <div className="status-indicator active">
            <span className="status-dot pulse"></span>
            System Active
          </div>
        </div>
      </header>

      {/* KPI Grid - Asymmetric layout */}
      <div className="kpi-grid">
        {/* Large featured KPI */}
        <div className="kpi-card kpi-featured" style={{ animationDelay: '0.1s' }}>
          <div className="kpi-header">
            <span className="kpi-icon">⬢</span>
            <span className="kpi-label">TOTAL FINDINGS</span>
            <HelpTooltip content="Total number of unique findings detected across all uploaded data sources." />
          </div>
          <div className="kpi-value-large">
            {numberFormatter.format(totalFindings)}
          </div>
          <div className="kpi-footer">
            <div className="kpi-bar">
              <div className="kpi-bar-fill" style={{ width: '100%' }}></div>
            </div>
          </div>
          <div className="card-glow glow-cyan"></div>
        </div>

        {/* Secondary KPIs */}
        <div className="kpi-card kpi-danger" style={{ animationDelay: '0.2s' }}>
          <div className="kpi-header">
            <span className="kpi-icon">▲</span>
            <span className="kpi-label">RISK SCORE</span>
            <HelpTooltip content="The sum of risk scores from all findings. A higher score indicates a higher overall risk." />
          </div>
          <div className="kpi-value">
            {numberFormatter.format(totalRiskScore)}
          </div>
          <div className="kpi-trend">
            <span className="trend-icon">↑</span>
            <span className="trend-text">ELEVATED</span>
          </div>
          <div className="card-glow glow-red"></div>
        </div>

        <div className="kpi-card kpi-warning" style={{ animationDelay: '0.3s' }}>
          <div className="kpi-header">
            <span className="kpi-icon">$</span>
            <span className="kpi-label">FINANCIAL EXPOSURE</span>
            <HelpTooltip content="The total estimated financial loss from all findings, calculated by the hybrid ML/LLM engine." />
          </div>
          <div className="kpi-value kpi-value-currency">
            {currencyFormatter.format(totalMoneyLoss)}
          </div>
          <div className="kpi-trend">
            <span className="trend-icon">⬤</span>
            <span className="trend-text">MONITORED</span>
          </div>
          <div className="card-glow glow-amber"></div>
        </div>

        <div className="kpi-card kpi-info" style={{ animationDelay: '0.4s' }}>
          <div className="kpi-header">
            <span className="kpi-icon">◉</span>
            <span className="kpi-label">ANALYSIS RUNS</span>
            <HelpTooltip content="The total number of analysis processes that have been run." />
          </div>
          <div className="kpi-value">
            {numberFormatter.format(totalAnalysisRuns)}
          </div>
          <div className="kpi-trend">
            <span className="trend-icon">→</span>
            <span className="trend-text">ACTIVE</span>
          </div>
          <div className="card-glow glow-blue"></div>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-panel" style={{ animationDelay: '0.5s' }}>
        <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />
      </div>

      {/* Charts Section */}
      <div className="charts-grid" style={{ animationDelay: '0.6s' }}>
        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◐</span>
            <h3 className="panel-title">Focus Area Distribution</h3>
          </div>
          <div className="panel-body">
            <FocusAreaChart data={focusAreaData} />
          </div>
          <div className="panel-grid"></div>
        </div>

        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◪</span>
            <h3 className="panel-title">Risk Level Analysis</h3>
          </div>
          <div className="panel-body">
            <RiskLevelChart data={riskLevelData} />
          </div>
          <div className="panel-grid"></div>
        </div>
      </div>

      {/* Money Loss Timeline */}
      {moneyLossData.length > 0 && (
        <div className="timeline-panel" style={{ animationDelay: '0.7s' }}>
          <div className="panel-header">
            <span className="panel-icon">▬</span>
            <h3 className="panel-title">Financial Exposure Timeline</h3>
          </div>
          <div className="panel-body">
            <MoneyLossChart data={moneyLossData} />
          </div>
          <div className="panel-grid"></div>
        </div>
      )}

      {/* Findings Table */}
      <div className="findings-panel" style={{ animationDelay: '0.8s' }}>
        <div className="panel-header">
          <div className="panel-header-left">
            <span className="panel-icon">▦</span>
            <h3 className="panel-title">Security Findings</h3>
          </div>
          <button
            className="action-button primary"
            onClick={() => navigate('/reports')}
          >
            <span className="button-icon">◈</span>
            Generate Report
          </button>
        </div>
        <div className="panel-body">
          <FindingsTable
            data={findings || []}
            onRowClick={handleFindingClick}
          />
        </div>
        <div className="panel-grid"></div>
      </div>
    </div>
  );
};

export default Dashboard;
