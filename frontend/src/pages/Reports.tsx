import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api, Finding, AnalysisRun } from '../services/api';
import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';
import DashboardFilters, { FilterState } from '../components/filters/DashboardFilters';

const Reports: React.FC = () => {
  const [filters, setFilters] = useState<FilterState>({
    focusArea: '',
    severity: '',
    status: '',
    dateFrom: '',
    dateTo: '',
  });

  const { data: findings, isLoading } = useQuery({
    queryKey: ['findings', filters],
    queryFn: () =>
      api.getFindings({
        focus_area: filters.focusArea || undefined,
        severity: filters.severity || undefined,
        status: filters.status || undefined,
        date_from: filters.dateFrom || undefined,
        date_to: filters.dateTo || undefined,
      }),
  });

  const { data: analysisRuns } = useQuery({
    queryKey: ['analysisRuns'],
    queryFn: api.getAnalysisRuns,
  });

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const exportToPDF = () => {
    if (!findings || findings.length === 0) return;

    const doc = new jsPDF();
    let yPos = 20;

    // Title
    doc.setFontSize(18);
    doc.text('Treasure Hunt Analyzer Report', 105, yPos, { align: 'center' });
    yPos += 10;

    // Summary
    doc.setFontSize(12);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 105, yPos, { align: 'center' });
    yPos += 10;
    doc.text(`Total Findings: ${findings.length}`, 105, yPos, { align: 'center' });
    yPos += 15;

    // Findings
    doc.setFontSize(14);
    doc.text('Findings:', 20, yPos);
    yPos += 10;

    doc.setFontSize(10);
    findings.forEach((finding: Finding, index: number) => {
      if (yPos > 280) {
        doc.addPage();
        yPos = 20;
      }

      doc.setFont('helvetica', 'bold');
      doc.text(`${index + 1}. ${finding.title}`, 20, yPos);
      yPos += 7;

      doc.setFont('helvetica', 'normal');
      doc.text(`Focus Area: ${finding.focus_area?.name || 'N/A'}`, 25, yPos);
      yPos += 5;
      doc.text(`Severity: ${finding.severity}`, 25, yPos);
      yPos += 5;
      doc.text(`Risk Score: ${finding.risk_assessment?.risk_score || 'N/A'}`, 25, yPos);
      yPos += 5;
      doc.text(
        `Money Loss: $${(finding.money_loss_calculation?.estimated_loss || 0).toLocaleString()}`,
        25,
        yPos
      );
      yPos += 5;
      if (finding.description) {
        const descLines = doc.splitTextToSize(finding.description, 170);
        doc.text(descLines, 25, yPos);
        yPos += descLines.length * 5;
      }
      yPos += 5;
    });

    doc.save('treasure-hunt-report.pdf');
  };

  const exportToExcel = () => {
    if (!findings || findings.length === 0) return;

    const worksheetData = findings.map((finding: Finding) => ({
      Title: finding.title,
      'Focus Area': finding.focus_area?.name || 'N/A',
      'Issue Type': finding.issue_type?.name || 'N/A',
      Severity: finding.severity,
      Status: finding.status,
      'Risk Score': finding.risk_assessment?.risk_score || 0,
      'Risk Level': finding.risk_assessment?.risk_level || 'N/A',
      'Money Loss': finding.money_loss_calculation?.estimated_loss || 0,
      'Detected At': new Date(finding.detected_at).toLocaleString(),
      Description: finding.description || '',
    }));

    const worksheet = XLSX.utils.json_to_sheet(worksheetData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Findings');

    // Add summary sheet
    const summaryData = [
      ['Report Summary'],
      ['Generated', new Date().toLocaleString()],
      ['Total Findings', findings.length],
      ['Total Money Loss', findings.reduce((sum: number, f: Finding) => 
        sum + (f.money_loss_calculation?.estimated_loss || 0), 0
      )],
    ];
    const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);
    XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary');

    XLSX.writeFile(workbook, 'treasure-hunt-report.xlsx');
  };

  if (isLoading) {
    return (
      <div className="text-center p-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  const totalMoneyLoss = findings?.reduce(
    (sum: number, f: Finding) => sum + (f.money_loss_calculation?.estimated_loss || 0),
    0
  ) || 0;

  return (
    <div className="container-fluid p-4">
      <h1 className="mb-4">Reports</h1>

      <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />

      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body text-center">
              <h5>Total Findings</h5>
              <h2>{findings?.length || 0}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body text-center">
              <h5>Total Money Loss</h5>
              <h2>${totalMoneyLoss.toLocaleString()}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body text-center">
              <h5>Export Options</h5>
              <div className="mt-2">
                <button className="btn btn-danger me-2" onClick={exportToPDF}>
                  Export PDF
                </button>
                <button className="btn btn-success" onClick={exportToExcel}>
                  Export Excel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Report Preview</h5>
        </div>
        <div className="card-body">
          <p>
            This report contains {findings?.length || 0} findings based on the current filters.
            Use the export buttons above to generate PDF or Excel reports with detailed risk
            explanations and money loss calculations.
          </p>

          {findings && findings.length > 0 && (
            <div className="mt-4">
              <h6>Summary by Focus Area:</h6>
              <ul>
                {Object.entries(
                  findings.reduce((acc: Record<string, number>, f: Finding) => {
                    const area = f.focus_area?.name || 'Unknown';
                    acc[area] = (acc[area] || 0) + 1;
                    return acc;
                  }, {})
                ).map(([area, count]) => (
                  <li key={area}>
                    {area}: {count} findings
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
