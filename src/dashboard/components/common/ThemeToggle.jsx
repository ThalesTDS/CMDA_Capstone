import React from 'react';
import {useTheme} from '../../contexts/ThemeContext';

const ThemeToggle = () => {
    const {theme, toggleTheme} = useTheme();

    return (
        <div className="flex items-center gap-2">
            {/* Theme icon and label */}
            <div className="flex items-center gap-1 text-sm font-medium">
                {theme === 'aquatic' ? (
                    <>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            className="w-4 h-4 text-primary"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                            />
                        </svg>
                        <span className="text-aquatic-text-primary">Aquatic</span>
                    </>
                ) : (
                    <>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            className="w-4 h-4 text-accent animate-pulse-slow"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                            />
                        </svg>
                        <span className="text-neon-text-primary">Neon</span>
                    </>
                )}
            </div>

            {/* Toggle switch */}
            <label className="relative inline-flex items-center cursor-pointer">
                <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={theme === 'neon'}
                    onChange={toggleTheme}
                />
                <div className={`
          w-12 h-6 rounded-full peer 
          ${theme === 'aquatic'
                    ? 'bg-aquatic-muted shadow-inner border border-primary/20'
                    : 'bg-neon-muted shadow-[0_0_8px_rgba(138,43,226,0.5)] border border-neon-border/50'
                }
          peer-focus:outline-none peer-focus:ring-2 
          peer-focus:ring-primary 
          peer-checked:after:translate-x-full 
          rtl:peer-checked:after:-translate-x-full 
          after:content-[''] 
          after:absolute after:top-[2px] after:start-[2px] 
          after:bg-white after:border-gray-300 
          after:border after:rounded-full after:h-5 after:w-5 
          after:transition-all
          ${theme === 'aquatic'
                    ? 'after:bg-primary/90 after:border-primary/50'
                    : 'after:bg-accent after:border-accent/80 after:shadow-[0_0_5px_rgba(0,255,255,0.7)]'
                }
        `}></div>
            </label>
        </div>
    );
};

export default ThemeToggle;