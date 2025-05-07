/**
 * Fetch metrics data from the server
 * @returns {Promise<string>} - CSV data as text
 */
export const fetchMetricsData = async () => {
  try {
    const response = await fetch('/api/metrics');
    
    if (!response.ok) {
      if (response.status === 404) {
        return { error: true, message: "No metrics data available yet. Please analyze a file first." };
      }
      throw new Error(`Failed to load metrics: ${response.statusText}`);
    }
    
    return await response.text();
  } catch (error) {
    console.error('API Error fetching metrics:', error);
    throw error;
  }
};

/**
 * Analyze a file or directory path
 * @param {string} rawPath - The file or directory path to analyze
 * @returns {Promise<Object>} - Analysis result indicating it started
 */
export const analyzePath = async (rawPath) => {
  const path = rawPath.replace(/\\/g, '/');   // keeps ProjectAnalyzer happy
  try {
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
    
    return await response.json();
  } catch (error) {
    console.error('API Error starting analysis:', error);
    throw error;
  }
};

/**
 * Check the status of an ongoing analysis
 * @returns {Promise<Object>} - Current analysis status
 */
export const getAnalysisStatus = async () => {
  try {
    const response = await fetch('/api/status');
    
    if (!response.ok) {
      throw new Error(`Failed to get analysis status: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error checking analysis status:', error);
    throw error;
  }
};

/**
 * Download metrics for a specific file
 * @param {string} fileId - The file identifier
 * @returns {Promise<Blob>} - CSV data as a blob
 */
export const downloadFileMetrics = async (fileId) => {
  try {
    const response = await fetch(`/api/download?file=${encodeURIComponent(fileId)}`);
    
    if (!response.ok) {
      throw new Error(`Failed to download metrics: ${response.statusText}`);
    }
    
    return await response.blob();
  } catch (error) {
    console.error('API Error downloading metrics:', error);
    throw error;
  }
};