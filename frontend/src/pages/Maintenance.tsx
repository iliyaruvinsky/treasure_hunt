import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';

interface DataSourceSummary {
  id: number;
  filename: string;
  data_type: string;
  status: string;
  upload_date: string | null;
  findings_count: number;
  file_size: number | null;
}

const Maintenance: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [showDeleteAll, setShowDeleteAll] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState('');

  const { data: dataSources, isLoading, error, refetch } = useQuery({
    queryKey: ['dataSources'],
    queryFn: api.getMaintenanceDataSources,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.deleteDataSource(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dataSources'] });
      queryClient.invalidateQueries({ queryKey: ['findings'] });
      queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
      queryClient.invalidateQueries({ queryKey: ['kpiSummary'] });
      setSelectedIds(new Set());
    },
  });

  const deleteAllMutation = useMutation({
    mutationFn: () => api.deleteAllDataSources(true),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dataSources'] });
      queryClient.invalidateQueries({ queryKey: ['findings'] });
      queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
      queryClient.invalidateQueries({ queryKey: ['kpiSummary'] });
      setShowDeleteAll(false);
      setDeleteConfirm('');
    },
  });

  const handleSelect = (id: number) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedIds.size === dataSources?.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(dataSources?.map((ds: DataSourceSummary) => ds.id) || []));
    }
  };

  const handleDeleteSelected = () => {
    if (selectedIds.size === 0) return;
    if (!window.confirm(`Are you sure you want to delete ${selectedIds.size} data source(s)? This will delete all related findings, alerts, and reports.`)) {
      return;
    }
    selectedIds.forEach(id => deleteMutation.mutate(id));
  };

  const handleDeleteAll = () => {
    if (deleteConfirm !== 'DELETE ALL') {
      alert('Please type "DELETE ALL" to confirm');
      return;
    }
    deleteAllMutation.mutate();
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
          <h4>Error loading data sources</h4>
          <p>{error instanceof Error ? error.message : 'Unknown error'}</p>
        </div>
      </div>
    );
  }

  const totalFindings = dataSources?.reduce((sum: number, ds: DataSourceSummary) => sum + ds.findings_count, 0) || 0;
  const totalSize = dataSources?.reduce((sum: number, ds: DataSourceSummary) => sum + (ds.file_size || 0), 0) || 0;

  return (
    <div className="container-fluid p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Data Maintenance</h1>
        <div>
          <button
            className="btn btn-danger me-2"
            onClick={() => setShowDeleteAll(true)}
            disabled={!dataSources || dataSources.length === 0}
          >
            Delete All Data
          </button>
        </div>
      </div>

      {/* Summary */}
      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Total Data Sources</h5>
              <h2>{dataSources?.length || 0}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Total Findings</h5>
              <h2>{totalFindings.toLocaleString()}</h2>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Total Size</h5>
              <h2>{(totalSize / 1024 / 1024).toFixed(2)} MB</h2>
            </div>
          </div>
        </div>
      </div>

      {/* Delete All Confirmation Modal */}
      {showDeleteAll && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header bg-danger text-white">
                <h5 className="modal-title">Delete All Data</h5>
                <button
                  type="button"
                  className="btn-close btn-close-white"
                  onClick={() => {
                    setShowDeleteAll(false);
                    setDeleteConfirm('');
                  }}
                ></button>
              </div>
              <div className="modal-body">
                <div className="alert alert-danger">
                  <strong>WARNING:</strong> This will permanently delete ALL data sources, findings, alerts, and reports.
                  This action cannot be undone!
                </div>
                <p>Type <strong>DELETE ALL</strong> to confirm:</p>
                <input
                  type="text"
                  className="form-control"
                  value={deleteConfirm}
                  onChange={(e) => setDeleteConfirm(e.target.value)}
                  placeholder="DELETE ALL"
                />
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowDeleteAll(false);
                    setDeleteConfirm('');
                  }}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleDeleteAll}
                  disabled={deleteAllMutation.isPending}
                >
                  {deleteAllMutation.isPending ? 'Deleting...' : 'Delete All'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Actions Bar */}
      {selectedIds.size > 0 && (
        <div className="alert alert-warning d-flex justify-content-between align-items-center mb-3">
          <span>{selectedIds.size} data source(s) selected</span>
          <button
            className="btn btn-danger btn-sm"
            onClick={handleDeleteSelected}
            disabled={deleteMutation.isPending}
          >
            Delete Selected
          </button>
        </div>
      )}

      {/* Data Sources Table */}
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Data Sources</h5>
          <button
            className="btn btn-sm btn-outline-primary"
            onClick={handleSelectAll}
          >
            {selectedIds.size === dataSources?.length ? 'Deselect All' : 'Select All'}
          </button>
        </div>
        <div className="card-body">
          {!dataSources || dataSources.length === 0 ? (
            <p className="text-muted">No data sources found.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th style={{ width: '40px' }}>
                      <input
                        type="checkbox"
                        checked={selectedIds.size === dataSources.length && dataSources.length > 0}
                        onChange={handleSelectAll}
                      />
                    </th>
                    <th>Filename</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Findings</th>
                    <th>Size</th>
                    <th>Upload Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {dataSources.map((ds: DataSourceSummary) => (
                    <tr key={ds.id}>
                      <td>
                        <input
                          type="checkbox"
                          checked={selectedIds.has(ds.id)}
                          onChange={() => handleSelect(ds.id)}
                        />
                      </td>
                      <td>{ds.filename}</td>
                      <td>
                        <span className={`badge ${ds.data_type === 'alert' ? 'bg-primary' : 'bg-info'}`}>
                          {ds.data_type}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${ds.status === 'completed' ? 'bg-success' : 'bg-danger'}`}>
                          {ds.status}
                        </span>
                      </td>
                      <td>{ds.findings_count.toLocaleString()}</td>
                      <td>{ds.file_size ? `${(ds.file_size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}</td>
                      <td>{ds.upload_date ? new Date(ds.upload_date).toLocaleString() : 'N/A'}</td>
                      <td>
                        <button
                          className="btn btn-sm btn-danger"
                          onClick={() => {
                            if (window.confirm(`Delete "${ds.filename}"? This will delete all related findings, alerts, and reports.`)) {
                              deleteMutation.mutate(ds.id);
                            }
                          }}
                          disabled={deleteMutation.isPending}
                        >
                          Delete
                        </button>
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

export default Maintenance;

