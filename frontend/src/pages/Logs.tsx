import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';

interface AuditLog {
  id: number;
  action: string;
  entity_type: string | null;
  entity_id: number | null;
  user_id: string | null;
  user_ip: string | null;
  user_agent: string | null;
  description: string | null;
  details: Record<string, any> | null;
  status: string | null;
  error_message: string | null;
  created_at: string;
}

const Logs: React.FC = () => {
  const [actionFilter, setActionFilter] = useState<string>('');
  const [entityTypeFilter, setEntityTypeFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  const { data: logs, isLoading, error, refetch } = useQuery({
    queryKey: ['auditLogs', actionFilter, entityTypeFilter, statusFilter],
    queryFn: () => api.getAuditLogs({
      action: actionFilter || undefined,
      entity_type: entityTypeFilter || undefined,
      status: statusFilter || undefined,
    }),
    refetchInterval: 5000, // Auto-refresh every 5 seconds
  });

  const getStatusBadge = (status: string | null) => {
    if (!status) return <span className="badge bg-secondary">Unknown</span>;
    switch (status.toLowerCase()) {
      case 'success':
        return <span className="badge bg-success">Success</span>;
      case 'error':
        return <span className="badge bg-danger">Error</span>;
      case 'partial':
        return <span className="badge bg-warning">Partial</span>;
      default:
        return <span className="badge bg-secondary">{status}</span>;
    }
  };

  const getActionBadge = (action: string) => {
    const colors: Record<string, string> = {
      upload: 'bg-primary',
      delete: 'bg-danger',
      analyze: 'bg-info',
      delete_all: 'bg-danger',
    };
    return <span className={`badge ${colors[action] || 'bg-secondary'}`}>{action}</span>;
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

  if (error) {
    return (
      <div className="container-fluid p-4">
        <div className="alert alert-danger">
          <h4>Error loading logs</h4>
          <p>{error instanceof Error ? error.message : 'Unknown error'}</p>
        </div>
      </div>
    );
  }

  const uniqueActions = Array.from(new Set(logs?.map((log: AuditLog) => log.action) || []));
  const uniqueEntityTypes = Array.from(new Set(logs?.map((log: AuditLog) => log.entity_type).filter(Boolean) || []));

  return (
    <div className="container-fluid p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Audit Logs</h1>
        <button className="btn btn-primary" onClick={() => refetch()}>
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="card mb-4">
        <div className="card-header">
          <h5 className="mb-0">Filters</h5>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-4">
              <label className="form-label">Action</label>
              <select
                className="form-select"
                value={actionFilter}
                onChange={(e) => setActionFilter(e.target.value)}
              >
                <option value="">All Actions</option>
                {uniqueActions.map((action) => (
                  <option key={action} value={action}>
                    {action}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label">Entity Type</label>
              <select
                className="form-select"
                value={entityTypeFilter}
                onChange={(e) => setEntityTypeFilter(e.target.value)}
              >
                <option value="">All Types</option>
                {uniqueEntityTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label">Status</label>
              <select
                className="form-select"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">All Statuses</option>
                <option value="success">Success</option>
                <option value="error">Error</option>
                <option value="partial">Partial</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Logs Table */}
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Log Entries ({logs?.length || 0})</h5>
        </div>
        <div className="card-body">
          {!logs || logs.length === 0 ? (
            <p className="text-muted">No logs found.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Action</th>
                    <th>Entity</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>User IP</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log: AuditLog) => (
                    <tr key={log.id}>
                      <td>{new Date(log.created_at).toLocaleString()}</td>
                      <td>{getActionBadge(log.action)}</td>
                      <td>
                        {log.entity_type && (
                          <span>
                            {log.entity_type}
                            {log.entity_id && ` #${log.entity_id}`}
                          </span>
                        )}
                      </td>
                      <td>{log.description || '-'}</td>
                      <td>{getStatusBadge(log.status)}</td>
                      <td>{log.user_ip || '-'}</td>
                      <td>
                        {log.details ? (
                          <button
                            className="btn btn-sm btn-outline-info"
                            onClick={() => {
                              alert(JSON.stringify(log.details, null, 2));
                            }}
                          >
                            View
                          </button>
                        ) : (
                          '-'
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Logs;

