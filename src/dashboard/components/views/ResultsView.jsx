import React from 'react';
import { useMetrics } from '../../contexts/MetricsContext';
import FileSelector from '../common/FileSelector';
import FileDetails from './FileDetails';
import ProjectOverview from './ProjectOverview';

const ResultsView = () => {
  const { metricsData, selectedFile, isLoading, error } = useMetrics();
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-76px)]">
        <div className="text-center">
          <svg className="animate-spin h-10 w-10 text-primary mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-lg font-medium">Loading metrics data...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-76px)]">
        <div className="bg-destructive/10 border border-destructive/30 p-6 rounded-lg max-w-xl mx-auto">
          <h2 className="text-xl font-bold text-destructive mb-2">Error Loading Data</h2>
          <p className="text-destructive">{error}</p>
          <button
            className="mt-4 px-4 py-2 bg-primary text-white rounded-md"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }
  
  if (!metricsData) {
    return null;
  }
  
  // Check if selected file is project level
  const isProjectView = metricsData.project.some(proj => proj.identifier === selectedFile);
  
  return (
    <div className="wrapper py-6">
      <div className="mb-6 flex justify-between items-center">
        <FileSelector />
        
        <button 
          className="btn-outline text-sm"
          onClick={() => {
            // Create download link for CSV
            // This is just a placeholder - would need to be implemented with the real API
            alert('Download functionality would be implemented here');
          }}
        >
          Export Metrics
        </button>
      </div>
      
      {isProjectView ? (
        <ProjectOverview />
      ) : (
        <FileDetails />
      )}
    </div>
  );
};

export default ResultsView;