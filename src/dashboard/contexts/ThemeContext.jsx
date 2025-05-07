import React, { createContext, useState, useContext, useEffect } from 'react';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  // Default to aquatic theme as specified in requirements
  const [theme, setTheme] = useState('aquatic');

  // Initialize theme from localStorage if available
  useEffect(() => {
    const savedTheme = localStorage.getItem('documetrics-theme');
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  // Update theme class on body and save to localStorage
  useEffect(() => {
    const root = document.documentElement;
    
    if (theme === 'neon') {
      root.classList.add('neon-theme');
    } else {
      root.classList.remove('neon-theme');
    }
    
    localStorage.setItem('documetrics-theme', theme);
  }, [theme]);

  // Toggle between aquatic and neon themes
  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'aquatic' ? 'neon' : 'aquatic'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};