import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const uploadMutation = useMutation({
    mutationFn: api.uploadFile,
    onSuccess: async (response) => {
      // Run analysis automatically after upload
      // The response contains data_source_id
      const dataSourceId = response.data_source_id || response.id;
      console.log('Upload successful, starting analysis for data source:', dataSourceId);
      
      try {
        const analysisRun = await api.runAnalysis(dataSourceId);
        console.log('Analysis completed:', analysisRun);
        // Invalidate and refetch queries
        await queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
        await queryClient.invalidateQueries({ queryKey: ['findings'] });
        // Refetch immediately
        await queryClient.refetchQueries({ queryKey: ['analysisRuns'] });
        await queryClient.refetchQueries({ queryKey: ['findings'] });
        // Wait a moment for data to be available
        setTimeout(() => {
          navigate('/');
        }, 1500);
      } catch (error: any) {
        console.error('Analysis failed:', error);
        // Show error but still navigate
        alert(`Upload successful but analysis failed: ${error?.message || 'Unknown error'}`);
        queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
        queryClient.invalidateQueries({ queryKey: ['findings'] });
        navigate('/');
      }
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploadProgress(50);
      await uploadMutation.mutateAsync(selectedFile);
      setUploadProgress(100);
      setTimeout(() => {
        setUploadProgress(0);
        setSelectedFile(null);
      }, 2000);
    } catch (error) {
      console.error('Upload failed:', error);
      setUploadProgress(0);
    }
  };

  return (
    <div className="container p-4">
      <h1 className="mb-4">Upload File</h1>

      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Upload Alert or Report</h5>
        </div>
        <div className="card-body">
          <div className="mb-3">
            <label className="form-label">Select File</label>
            <input
              type="file"
              className="form-control"
              accept=".pdf,.csv,.docx,.xlsx"
              onChange={handleFileChange}
            />
            <small className="form-text text-muted">
              Supported formats: PDF, CSV, DOCX, XLSX (Skywind 4C or SoDA)
            </small>
          </div>

          {selectedFile && (
            <div className="mb-3">
              <p><strong>Selected:</strong> {selectedFile.name}</p>
              <p><strong>Size:</strong> {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}

          {uploadProgress > 0 && (
            <div className="mb-3">
              <div className="progress">
                <div
                  className="progress-bar"
                  role="progressbar"
                  style={{ width: `${uploadProgress}%` }}
                >
                  {uploadProgress}%
                </div>
              </div>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={!selectedFile || uploadMutation.isPending}
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload & Analyze'}
          </button>

          {uploadMutation.isError && (
            <div className="alert alert-danger mt-3">
              Upload failed: {uploadMutation.error instanceof Error ? uploadMutation.error.message : 'Unknown error'}
            </div>
          )}

          {uploadMutation.isSuccess && (
            <div className="alert alert-success mt-3">
              File uploaded and analysis started successfully!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Upload;
