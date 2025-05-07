import React, { useState } from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const NativeDialogButton = ({ onSelectPath, isLoading = false, className = '' }) => {
  const { theme } = useTheme();
  const [selectedPath, setSelectedPath] = useState('');
  const [error, setError] = useState('');
  
  const handleOpenDialog = async () => {
    if (isLoading) return;
    
    setError('');
    
    try {
      // Call the backend API to open the native file dialog
      const response = await fetch('/api/file-dialog');
      
      if (!response.ok) {
        throw new Error('Failed to open file dialog');
      }
      
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
        return;
      }
      
      if (data.path) {
        const unixPath = data.path.replace(/\\+/g, '/');
        setSelectedPath(unixPath);
        onSelectPath?.(unixPath);
      }
    } catch (err) {
      console.error('Error opening file dialog:', err);
      setError('Failed to open file dialog');
    }
  };
  
  const buttonClasses = `
    relative overflow-hidden px-6 py-3 text-lg rounded-lg cursor-pointer 
    inline-block transition-all duration-300 
    ${isLoading ? 'opacity-75 cursor-not-allowed' : 'hover:shadow-lg'} 
    ${theme === 'neon' 
      ? 'bg-neon-primary text-white shadow-[0_0_15px_rgba(138,43,226,0.5)]' 
      : 'bg-primary text-white shadow-md'
    }
  `;
  
  return (
    <div className={`${className}`}>
      <button
        type="button"
        onClick={handleOpenDialog}
        disabled={isLoading}
        className={buttonClasses}
      >
        <span className="flex items-center justify-center gap-3">
          {isLoading ? (
            <>
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </>
          ) : (
            <>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path 
                  d="M10 3H4C3.44772 3 3 3.44772 3 4V20C3 20.5523 3.44772 21 4 21H20C20.5523 21 21 20.5523 21 20V14" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                />
                <path 
                  d="M16 3H21V8" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                />
                <path 
                  d="M21 3L12 12" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                />
              </svg>
              Select File or Folder
            </>
          )}
        </span>
      </button>
      
      {selectedPath && (
        <div className="mt-2 text-sm text-muted-foreground">
          Selected: <span className="font-medium">{selectedPath}</span>
        </div>
      )}
      
      {error && (
        <div className="mt-2 text-sm text-destructive">
          {error}
        </div>
      )}
    </div>
  );
};

export default NativeDialogButton;
