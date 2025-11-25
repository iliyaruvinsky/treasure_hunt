import React from 'react';

export interface FilterState {
  focusArea: string;
  severity: string;
  status: string;
  dateFrom: string;
  dateTo: string;
}

interface DashboardFiltersProps {
  filters: FilterState;
  onFilterChange: (filters: Partial<FilterState>) => void;
}

const DashboardFilters: React.FC<DashboardFiltersProps> = ({
  filters,
  onFilterChange,
}) => {
  const focusAreas = [
    { value: '', label: 'All Focus Areas' },
    { value: 'BUSINESS_PROTECTION', label: 'Business Protection' },
    { value: 'BUSINESS_CONTROL', label: 'Business Control' },
    { value: 'ACCESS_GOVERNANCE', label: 'Access Governance' },
    { value: 'TECHNICAL_CONTROL', label: 'Technical Control' },
    { value: 'JOBS_CONTROL', label: 'Jobs Control' },
    { value: 'S4HANA_EXCELLENCE', label: 'S/4HANA Excellence' },
  ];

  const severities = [
    { value: '', label: 'All Severities' },
    { value: 'Critical', label: 'Critical' },
    { value: 'High', label: 'High' },
    { value: 'Medium', label: 'Medium' },
    { value: 'Low', label: 'Low' },
  ];

  const statuses = [
    { value: '', label: 'All Statuses' },
    { value: 'new', label: 'New' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'resolved', label: 'Resolved' },
    { value: 'false_positive', label: 'False Positive' },
  ];

  return (
    <div className="card mb-4">
      <div className="card-header">
        <h5 className="mb-0">Filters</h5>
      </div>
      <div className="card-body">
        <div className="row g-3">
          <div className="col-md-3">
            <label className="form-label">Focus Area</label>
            <select
              className="form-select"
              value={filters.focusArea}
              onChange={(e) => onFilterChange({ focusArea: e.target.value })}
            >
              {focusAreas.map((fa) => (
                <option key={fa.value} value={fa.value}>
                  {fa.label}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-2">
            <label className="form-label">Severity</label>
            <select
              className="form-select"
              value={filters.severity}
              onChange={(e) => onFilterChange({ severity: e.target.value })}
            >
              {severities.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-2">
            <label className="form-label">Status</label>
            <select
              className="form-select"
              value={filters.status}
              onChange={(e) => onFilterChange({ status: e.target.value })}
            >
              {statuses.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-2">
            <label className="form-label">Date From</label>
            <input
              type="date"
              className="form-control"
              value={filters.dateFrom}
              onChange={(e) => onFilterChange({ dateFrom: e.target.value })}
            />
          </div>
          <div className="col-md-2">
            <label className="form-label">Date To</label>
            <input
              type="date"
              className="form-control"
              value={filters.dateTo}
              onChange={(e) => onFilterChange({ dateTo: e.target.value })}
            />
          </div>
          <div className="col-md-1 d-flex align-items-end">
            <button
              className="btn btn-secondary w-100"
              onClick={() =>
                onFilterChange({
                  focusArea: '',
                  severity: '',
                  status: '',
                  dateFrom: '',
                  dateTo: '',
                })
              }
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardFilters;

