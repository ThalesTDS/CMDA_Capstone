import React, { useState, useEffect } from 'react';
import { useMetrics } from '../../contexts/MetricsContext';
import { formatFileName } from '../../utils/utils';
import { useTheme } from '../../contexts/ThemeContext';
import GaugeChart from '../charts/GaugeChart';
import RadarChart from '../charts/RadarChart';
import SummaryStats from '../charts/SummaryStats';

const FileDetails = () => {
  const { selectedFile, getFileMetrics } = useMetrics();
  const { theme } = useTheme();
  const [showMetrics, setShowMetrics] = useState(false);
  
  // Animation timing
  useEffect(() => {
    setShowMetrics(false);
    const timer = setTimeout(() => {
      setShowMetrics(true);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [selectedFile]);
  
  const metrics = getFileMetrics(selectedFile);
  
  if (!metrics) {
    return (
      <div className="p-6 text-center animate-pulse">
        <p className="text-muted-foreground">No file selected or file data not available</p>
      </div>
    );
  }
  
  const metricKeys = ['comment_density', 'completeness', 'conciseness', 'accuracy'];
  const cardClasses = `${theme === 'neon' ? 'bg-card/80 border border-neon-border/40 shadow-[0_8px_30px_rgba(0,0,0,0.12)]' : 'bg-card border border-primary/10 shadow-lg'} rounded-xl backdrop-blur-sm transition-all duration-500`;
  
  return (
    <div className={`p-6 ${theme === 'neon' ? 'bg-gradient-to-b from-background to-neon-primary/10' : 'bg-gradient-to-b from-background to-primary/5'}`}>
      {/* Background elements */}
      {theme === 'neon' && (
        <div className="absolute inset-0 overflow-hidden z-0 pointer-events-none opacity-30">
          <div className="absolute h-64 w-64 rounded-full bg-purple-500/20 blur-3xl top-10 -left-20"></div>
          <div className="absolute h-96 w-96 rounded-full bg-cyan-500/20 blur-3xl bottom-10 -right-20"></div>
        </div>
      )}
      
      {/* Header with file name */}
      <div className="relative z-10">
        <div className="flex justify-between items-center mb-8">
          <h2 className={`text-3xl font-bold ${theme === 'neon' ? 'text-accent' : ''}`}>
            {formatFileName(metrics.identifier)}
            <div className={`h-1 w-20 mt-2 ${theme === 'neon' ? 'bg-accent' : 'bg-primary'} rounded-full`}></div>
          </h2>
          
          <div 
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              metrics.doc_type === 'Human' 
                ? theme === 'neon' ? 'bg-purple-900/60 text-purple-100' : 'bg-blue-100 text-blue-800'
                : theme === 'neon' ? 'bg-cyan-900/60 text-cyan-100' : 'bg-green-100 text-green-800'
            }`}
          >
            {metrics.doc_type} Documentation
          </div>
        </div>
        
        {/* Summary and Radar */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className={`lg:col-span-1 ${cardClasses} p-6 ${showMetrics ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'} transition-all duration-500 delay-100`}>
            <h3 className={`text-xl font-semibold mb-4 ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>Summary</h3>
            <SummaryStats metrics={metrics} />
          </div>
          
          <div className={`lg:col-span-2 ${cardClasses} p-6 ${showMetrics ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'} transition-all duration-500 delay-200`}>
            <h3 className={`text-xl font-semibold mb-4 ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>Documentation Profile</h3>
            <div className="h-64">
              <RadarChart 
                data={metrics} 
                title="" 
              />
            </div>
            <div className="mt-4 text-center text-sm text-muted-foreground">
              Hover over the chart points for detailed metrics
            </div>
          </div>
        </div>
        
        {/* Gauge charts */}
        <div className={`${cardClasses} p-6 ${showMetrics ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'} transition-all duration-500 delay-300`}>
          <h3 className={`text-xl font-semibold mb-6 ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>Individual Metrics</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {metricKeys.map((metric, index) => (
              <div key={metric} className="flex flex-col items-center">
                <GaugeChart 
                  metric={metric} 
                  value={metrics[metric]} 
                  size={250}
                />
                <p className="mt-2 text-sm text-muted-foreground text-center max-w-xs">
                  {getMetricDescription(metric)}
                </p>
              </div>
            ))}
          </div>
        </div>
        
        {/* File code info */}
        <div className={`mt-6 ${cardClasses} p-6 ${showMetrics ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'} transition-all duration-500 delay-400`}>
          <h3 className={`text-xl font-semibold mb-4 ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>Code Statistics</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className={`p-4 rounded-lg ${theme === 'neon' ? 'bg-neon-muted' : 'bg-aquatic-muted'}`}>
              <div className="text-sm text-muted-foreground mb-1">Lines of Code</div>
              <div className="text-2xl font-bold">{metrics.line_count}</div>
            </div>
            
            <div className={`p-4 rounded-lg ${theme === 'neon' ? 'bg-neon-muted' : 'bg-aquatic-muted'}`}>
              <div className="text-sm text-muted-foreground mb-1">Comment Density</div>
              <div className="text-2xl font-bold">{(metrics.comment_density * 100).toFixed(1)}%</div>
            </div>
            
            <div className={`p-4 rounded-lg ${theme === 'neon' ? 'bg-neon-muted' : 'bg-aquatic-muted'}`}>
              <div className="text-sm text-muted-foreground mb-1">Documentation Quality</div>
              <div className="flex items-center">
                <div className="text-2xl font-bold mr-2">{metrics.overall_score.toFixed(2)}</div>
                <RatingStars rating={Math.round(metrics.overall_score * 5)} />
              </div>
            </div>
            
            <div className={`p-4 rounded-lg ${theme === 'neon' ? 'bg-neon-muted' : 'bg-aquatic-muted'}`}>
              <div className="text-sm text-muted-foreground mb-1">Path</div>
              <div className="text-sm font-medium truncate">{metrics.identifier}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper component for star ratings
const RatingStars = ({ rating }) => {
  const { theme } = useTheme();
  const maxStars = 5;
  
  return (
    <div className="flex">
      {[...Array(maxStars)].map((_, i) => (
        <svg
          key={i}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill={i < rating ? (theme === 'neon' ? '#00FFFF' : '#0072B5') : 'none'}
          stroke={theme === 'neon' ? '#00FFFF' : '#0072B5'}
          className="w-4 h-4"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1}
            d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          />
        </svg>
      ))}
    </div>
  );
};

// Helper for metric descriptions
const getMetricDescription = (metric) => {
  switch (metric) {
    case 'comment_density':
      return 'Measures the ratio of comments to code in the file';
    case 'completeness':
      return 'Evaluates how thoroughly the code is documented';
    case 'conciseness':
      return 'Measures how efficiently the documentation conveys information';
    case 'accuracy':
      return 'Assesses how well the documentation matches the code it describes';
    default:
      return '';
  }
};

export default FileDetails;