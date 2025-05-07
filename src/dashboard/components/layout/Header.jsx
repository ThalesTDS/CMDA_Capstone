import React, { useState, useEffect } from 'react';
import ThemeToggle from '../common/ThemeToggle';
import { useMetrics } from '../../contexts/MetricsContext';
import { useTheme } from '../../contexts/ThemeContext';

// Nautical compass animation component
const CompassAnimation = () => {
  const { theme } = useTheme();
  
  return (
    <div className="hidden md:block absolute right-20 top-1/2 transform -translate-y-1/2 pointer-events-none">
      <svg
        width="40"
        height="40"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={`opacity-30 animate-rotate-slow ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}
        strokeWidth="1"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="12" cy="12" r="10"></circle>
        <polygon className="compass-needle" points="12 2, 12 22, 12 2, 2 12, 22 12" strokeWidth="1"></polygon>
        <path d="M16.24 7.76a6 6 0 010 8.49m-8.48-.01a6 6 0 010-8.49m11.31-2.82a10 10 0 010 14.14m-14.14 0a10 10 0 010-14.14"></path>
      </svg>
    </div>
  );
};

// Wave header decoration
const HeaderWave = () => {
  const { theme } = useTheme();
  
  return (
    <div className="absolute bottom-0 left-0 right-0 h-2 overflow-hidden">
      <div className={`wave wave1 ${theme === 'aquatic' ? 'bg-primary/20' : 'bg-accent/20'}`}></div>
    </div>
  );
};

// Animated logo with home link and tooltip
const AnimatedLogo = () => {
  const { theme } = useTheme();
  const [showTooltip, setShowTooltip] = useState(false);
  
  return (
    <a 
      href="/"
      className="flex items-center group relative" 
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        className={`w-8 h-8 mr-3 ${theme === 'neon' ? 'text-accent animate-pulse-slow' : 'text-primary'} transition-transform group-hover:scale-110`}
        strokeWidth="1.5" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      >
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
      </svg>
      <div>
        <h1 className="text-xl font-bold text-foreground flex items-center">
          DocuMetrics
          <span className={`ml-1 inline-block w-2 h-2 rounded-full ${theme === 'neon' ? 'bg-accent' : 'bg-primary'} animate-ping-slow`}></span>
        </h1>
        <p className={`text-xs ${theme === 'neon' ? 'text-accent/70' : 'text-primary/70'}`}>NAVSEA Documentation Evaluation</p>
      </div>
      
      {/* Tooltip */}
      {showTooltip && (
        <div 
          className={`absolute -bottom-8 left-0 px-2 py-1 text-xs rounded ${theme === 'neon' ? 'bg-neon-surface text-accent border border-neon-border' : 'bg-white text-primary shadow-md'} z-50 whitespace-nowrap`}
        >
          Click to return home
        </div>
      )}
    </a>
  );
};

const Header = () => {
  const { metricsData, isLoading } = useMetrics();
  const { theme } = useTheme();
  const [scrolled, setScrolled] = useState(false);
  
  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  const handleNewAnalysis = () => {
    // Create a custom event to trigger new analysis
    const event = new CustomEvent('documetricsNewAnalysis');
    window.dispatchEvent(event);
  };
  
  return (
    <header 
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled 
          ? 'bg-card/90 backdrop-blur-md shadow-md py-2' 
          : 'bg-card py-4'
      } relative`}
    >
      <div className="wrapper">
        <div className="flex justify-between items-center">
          <AnimatedLogo />
          
          <div className="flex items-center gap-4">
            {/* Show the "New Analysis" button only after first analysis */}
            {metricsData && (
              <button
                onClick={handleNewAnalysis}
                disabled={isLoading}
                className={`btn-primary text-sm group relative overflow-hidden ${
                  theme === 'neon' ? 'shadow-[0_0_8px_rgba(0,255,255,0.3)]' : ''
                }`}
              >
                <span className="relative z-10">
                  {isLoading ? 'Analyzing...' : 'New Analysis'}
                </span>
                <span className={`absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity ${
                  theme === 'aquatic' ? 'bg-secondary' : 'bg-accent'
                }`}></span>
              </button>
            )}
            
            <ThemeToggle />
          </div>
        </div>
      </div>
      
      <CompassAnimation />
      <HeaderWave />
    </header>
  );
};

export default Header;