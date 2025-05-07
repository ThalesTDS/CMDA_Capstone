import React, { createContext, useState, useContext } from 'react';
import { parseCSV, groupMetricsByLevel } from '../utils/utils';

const MetricsContext = createContext();

export const MetricsProvider = ({ children }) => {
  const [metricsData, setMetricsData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load metrics from CSV
  const loadMetricsFromCSV = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch('/api/metrics');
      
      if (!response.ok) {
        throw new Error(`Failed to load metrics: ${response.statusText}`);
      }
      
      const csvText = await response.text();
      const parsedData = parseCSV(csvText);
      const groupedData = groupMetricsByLevel(parsedData);
      
      setMetricsData(groupedData);
      
      // Select the first file by default if available
      if (groupedData.file.length > 0) {
        setSelectedFile(groupedData.file[0].identifier);
      } else if (groupedData.project.length > 0) {
        setSelectedFile(groupedData.project[0].identifier);
      }
      
      setIsLoading(false);
    } catch (err) {
      console.error('Error loading metrics:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  // Analyze a file or directory path
  const analyzePath = async (path) => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Start the analysis
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ path }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to start analysis');
      }
      
      // Start polling for status updates
      await pollAnalysisStatus();
      
    } catch (err) {
      console.error('Error analyzing path:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };
  
  // Poll for analysis status updates
  const pollAnalysisStatus = async () => {
    try {
      let completed = false;
      let attempts = 0;
      const maxAttempts = 60; // 5 minutes maximum (with 5s intervals)
      
      while (!completed && attempts < maxAttempts) {
        const response = await fetch('/api/status');
        if (!response.ok) {
          throw new Error('Failed to fetch analysis status');
        }
        
        const status = await response.json();
        
        if (status.error) {
          throw new Error(status.error);
        }
        
        if (!status.in_progress) {
          completed = true;
          if (status.result && status.result.code === 0) {
            // Analysis completed successfully, load the metrics
            await loadMetricsFromCSV();
          } else {
            throw new Error(status.result?.message || 'Analysis failed');
          }
        } else {
          // Update progress information
          // This could be used to show a progress bar
          console.log(`Analysis progress: ${status.progress}% - ${status.status_message}`);
          
          // Wait before polling again
          await new Promise(resolve => setTimeout(resolve, 5000));
        }
        
        attempts++;
      }
      
      if (!completed) {
        throw new Error('Analysis timed out');
      }
      
      setIsLoading(false);
    } catch (err) {
      console.error('Error during analysis polling:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  // Get metrics for a specific file
  const getFileMetrics = (fileId) => {
    if (!metricsData) return null;
    
    const fileMetrics = metricsData.file.find(metric => metric.identifier === fileId);
    return fileMetrics || null;
  };

  // Get project metrics
  const getProjectMetrics = () => {
    if (!metricsData || metricsData.project.length === 0) return null;
    
    return metricsData.project[0];
  };

  return (
    <MetricsContext.Provider
      value={{
        metricsData,
        selectedFile,
        setSelectedFile,
        isLoading,
        error,
        loadMetricsFromCSV,
        analyzePath,
        getFileMetrics,
        getProjectMetrics,
      }}
    >
      {children}
    </MetricsContext.Provider>
  );
};

export const useMetrics = () => {
  const context = useContext(MetricsContext);
  if (context === undefined) {
    throw new Error('useMetrics must be used within a MetricsProvider');
  }
  return context;
};