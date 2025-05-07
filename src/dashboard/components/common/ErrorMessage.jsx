import React from 'react';

const ErrorMessage = ({ 
  message, 
  actionText = 'Try Again', 
  onAction = () => window.location.reload() 
}) => {
  if (!message) return null;
  
  return (
    <div className="bg-destructive/10 border border-destructive/30 p-4 rounded-md">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-destructive" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 11-2 0 1 1 0 012 0zm-1 6a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm font-medium text-destructive">
            {message}
          </p>
          {actionText && (
            <div className="mt-4">
              <button
                type="button"
                className="btn-primary text-sm"
                onClick={onAction}
              >
                {actionText}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;