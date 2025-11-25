import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api, Finding } from '../services/api';

const FindingDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: findings, isLoading } = useQuery({
    queryKey: ['findings'],
    queryFn: api.getFindings,
  });

  const finding = findings?.find((f: Finding) => f.id === parseInt(id || '0'));

  if (isLoading) {
    return (
      <div className="text-center p-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!finding) {
    return (
      <div className="container p-5">
        <div className="alert alert-warning">
          Finding not found
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/findings')}>
          Back to Findings
        </button>
      </div>
    );
  }

  return (
    <div className="container p-4">
      <button className="btn btn-secondary mb-3" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <div className="card">
        <div className="card-header">
          <h2>{finding.title}</h2>
        </div>
        <div className="card-body">
          <div className="row mb-3">
            <div className="col-md-6">
              <h5>Details</h5>
              <table className="table">
                <tbody>
                  <tr>
                    <td><strong>Focus Area:</strong></td>
                    <td>{finding.focus_area?.name || 'N/A'}</td>
                  </tr>
                  <tr>
                    <td><strong>Issue Type:</strong></td>
                    <td>{finding.issue_type?.name || 'N/A'}</td>
                  </tr>
                  <tr>
                    <td><strong>Severity:</strong></td>
                    <td>
                      <span className={`badge bg-${
                        finding.severity === 'Critical' ? 'danger' :
                        finding.severity === 'High' ? 'warning' :
                        finding.severity === 'Medium' ? 'info' : 'success'
                      }`}>
                        {finding.severity}
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td><strong>Status:</strong></td>
                    <td>{finding.status}</td>
                  </tr>
                  <tr>
                    <td><strong>Detected At:</strong></td>
                    <td>{new Date(finding.detected_at).toLocaleString()}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="col-md-6">
              <h5>Risk Assessment</h5>
              {finding.risk_assessment ? (
                <table className="table">
                  <tbody>
                    <tr>
                      <td><strong>Risk Score:</strong></td>
                      <td>{finding.risk_assessment.risk_score}</td>
                    </tr>
                    <tr>
                      <td><strong>Risk Level:</strong></td>
                      <td>{finding.risk_assessment.risk_level}</td>
                    </tr>
                  </tbody>
                </table>
              ) : (
                <p className="text-muted">No risk assessment available</p>
              )}

              <h5 className="mt-4">Money Loss</h5>
              {finding.money_loss_calculation ? (
                <table className="table">
                  <tbody>
                    <tr>
                      <td><strong>Estimated Loss:</strong></td>
                      <td>${finding.money_loss_calculation.estimated_loss.toLocaleString()}</td>
                    </tr>
                    <tr>
                      <td><strong>Confidence:</strong></td>
                      <td>{(finding.money_loss_calculation.confidence * 100).toFixed(1)}%</td>
                    </tr>
                  </tbody>
                </table>
              ) : (
                <p className="text-muted">No money loss calculation available</p>
              )}
            </div>
          </div>

          <div className="mb-3">
            <h5>Description</h5>
            <p>{finding.description || 'No description available'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FindingDetail;

