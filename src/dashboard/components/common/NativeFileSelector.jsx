import React, { useRef, useState } from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const NativeFileSelector = ({ onSelect, isDirectory = false, isLoading = false, className = '' }) => {
  const { theme } = useTheme();
  const fileInputRef = useRef(null);
  const [selectedPath, setSelectedPath] = useState('');
  
  const handleClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  
  const handleChange = (e) => {
    // Get the selected files
    const files = e.target.files;
    
    if (files && files.length > 0) {
      // For directories, we may have multiple files
      if (isDirectory) {
        // Get the common directory path
        // This extracts the path until the last directory from the first file
        const filePath = files[0].webkitRelativePath;
        const dirPath = filePath.split('/')[0];
        
        // In a real implementation, we'd need to get the full path
        // Here we're showing what we can access from the browser
        setSelectedPath(dirPath);
        onSelect(dirPath);
      } else {
        // For a single file, just return the file and its path
        const file = files[0];
        
        // In browsers, we can only get the filename for security reasons
        setSelectedPath(file.name);
        
        // In a real application, we'd need backend support to translate this
        // relative path into an absolute one
        onSelect(file.name);
      }
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
  
  const iconColor = theme === 'neon' ? '#00FFFF' : '#FFFFFF';
  
  return (
    <div className={`${className}`}>
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={handleChange}
        disabled={isLoading}
        {...(isDirectory ? { webkitdirectory: "", directory: "" } : {})}
      />
      
      <button
        type="button"
        onClick={handleClick}
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
                {isDirectory ? (
                  // Folder icon
                  <path 
                    d="M3 7V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V9C21 7.89543 20.1046 7 19 7H13L11 5H5C3.89543 5 3 5.89543 3 7Z" 
                    stroke={iconColor} 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  />
                ) : (
                  // File icon
                  <>
                    <path 
                      d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" 
                      stroke={iconColor} 
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    />
                    <path 
                      d="M14 2V8H20" 
                      stroke={iconColor} 
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    />
                  </>
                )}
              </svg>
              {isDirectory ? 'Select Folder' : 'Select File'}
            </>
          )}
        </span>
      </button>
      
      {selectedPath && (
        <div className="mt-2 text-sm text-muted-foreground">
          Selected: <span className="font-medium">{selectedPath}</span>
        </div>
      )}
    </div>
  );
};

export default NativeFileSelector;