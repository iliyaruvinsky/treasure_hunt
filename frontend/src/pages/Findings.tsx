import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api, Finding } from '../services/api';
import FindingsTable from '../components/tables/FindingsTable';
import DashboardFilters, { FilterState } from '../components/filters/DashboardFilters';

const Findings: React.FC = () => {
  const navigate = useNavigate();
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

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const handleFindingClick = (finding: Finding) => {
    navigate(`/findings/${finding.id}`);
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

  return (
    <div className="container-fluid p-4">
      <h1 className="mb-4">Findings</h1>

      <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">All Findings ({findings?.length || 0})</h5>
        </div>
        <div className="card-body">
          <FindingsTable
            data={findings || []}
            onRowClick={handleFindingClick}
          />
        </div>
      </div>
    </div>
  );
};

export default Findings;
