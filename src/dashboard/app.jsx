import React, { useEffect, useState } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import { MetricsProvider, useMetrics } from './contexts/MetricsContext';
import MainLayout from './components/layout/MainLayout';
import WelcomePage from './components/views/WelcomePage';
import ResultsView from './components/views/ResultsView';

// Main app content component (wrapped with context providers in the exported App)
const AppContent = () => {
  const { metricsData, loadMetricsFromCSV, analyzePath } = useMetrics();
  const [showWelcome, setShowWelcome] = useState(true);
  
  // Try to load metrics data on mount, but don't show error if none exists yet
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        await loadMetricsFromCSV();
        setShowWelcome(false);
      } catch (error) {
        console.log('No previous metrics data found');
        // This is expected for first run, so we just stay on welcome page
      }
    };
    
    loadInitialData();
  }, []);
  
  // Listen for new analysis events from the header component
  useEffect(() => {
    const handleNewAnalysisEvent = () => {
      setShowWelcome(true);
    };
    
    window.addEventListener('documetricsNewAnalysis', handleNewAnalysisEvent);
    
    return () => {
      window.removeEventListener('documetricsNewAnalysis', handleNewAnalysisEvent);
    };
  }, []);
  
  // Determine which view to show based on the URL path
  const isOnDashboardPage = () => {
    return window.location.pathname === '/dashboard';
  };
  
  useEffect(() => {
    // If user navigates to /dashboard but there's no data, load welcome page
    if (isOnDashboardPage() && !metricsData) {
      loadMetricsFromCSV().catch(() => {
        // If there's no data available, redirect to home
        window.location.href = '/';
      });
    }
  }, []);
  
  return (
    <MainLayout>
      {(isOnDashboardPage() && metricsData) ? <ResultsView /> : <WelcomePage />}
    </MainLayout>
  );
};

// Top-level App component with all providers
const App = () => {
  return (
    <ThemeProvider>
      <MetricsProvider>
        <AppContent />
      </MetricsProvider>
    </ThemeProvider>
  );
};

export default App;