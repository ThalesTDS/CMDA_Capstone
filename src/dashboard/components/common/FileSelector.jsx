import React, {useEffect, useRef, useState} from 'react';
import {useMetrics} from '../../contexts/MetricsContext';
import {useTheme} from '../../contexts/ThemeContext';
import {formatFileName} from '../../utils/utils';

const FileSelector = () => {
    const {metricsData, selectedFile, setSelectedFile} = useMetrics();
    const {theme} = useTheme();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    if (!metricsData) return null;

    const getFileOptions = () => {
        const options = [];

        // Add project level option first if it exists
        if (metricsData.project && metricsData.project.length > 0) {
            options.push({
                id: metricsData.project[0].identifier,
                label: 'Project Results',
                type: metricsData.project[0].doc_type,
                level: 'project'
            });
        }

        // Add file level options
        if (metricsData.file && metricsData.file.length > 0) {
            const fileOptions = metricsData.file.map(file => ({
                id: file.identifier,
                label: formatFileName(file.identifier),
                type: file.doc_type,
                level: 'file'
            }));

            options.push(...fileOptions);
        }

        return options;
    };

    const options = getFileOptions();
    const selectedOption = options.find(option => option.id === selectedFile) || options[0];

    const handleSelectOption = (option) => {
        setSelectedFile(option.id);
        setIsOpen(false);
    };

    const getBadgeClass = (docType) => {
        if (theme === 'neon') {
            return docType === 'Human'
                ? 'bg-purple-900/60 text-purple-100'
                : 'bg-cyan-900/60 text-cyan-100';
        } else {
            return docType === 'Human'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-green-100 text-green-800';
        }
    };

    const getSelectedOptionLabel = () => {
        if (!selectedOption) return 'Select file';

        return (
            <div className="flex items-center justify-between w-full">
                <div className="truncate max-w-[200px]">{selectedOption.label}</div>
                <div className={`px-2 py-0.5 rounded text-xs font-medium ${getBadgeClass(selectedOption.type)}`}>
                    {selectedOption.level === 'project' ? 'Project' : selectedOption.type}
                </div>
            </div>
        );
    };

    return (
        <div ref={dropdownRef} className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
          flex items-center justify-between w-64 px-4 py-2 text-sm rounded-lg
          ${isOpen ? 'outline-none ring-2' : ''}
          ${theme === 'neon'
                    ? 'bg-neon-surface border border-neon-border/50 hover:bg-neon-muted text-neon-text-primary ring-accent/70'
                    : 'bg-white border border-primary/20 hover:bg-aquatic-muted/30 text-aquatic-text-primary ring-primary/50'
                }
        `}
            >
                {getSelectedOptionLabel()}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className={`h-4 w-4 ml-1 transition-transform ${isOpen ? 'transform rotate-180' : ''}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7"/>
                </svg>
            </button>

            {isOpen && (
                <div
                    className={`
            absolute z-50 mt-1 w-full rounded-lg shadow-lg 
            ${theme === 'neon'
                        ? 'bg-neon-surface border border-neon-border/50 shadow-[0_5px_15px_rgba(0,0,0,0.3)]'
                        : 'bg-white border border-primary/20'
                    } 
            max-h-60 overflow-auto
          `}
                >
                    <ul className="py-1">
                        {options.map((option) => (
                            <li
                                key={option.id}
                                onClick={() => handleSelectOption(option)}
                                className={`
                  px-4 py-2 text-sm cursor-pointer flex justify-between items-center
                  ${selectedFile === option.id
                                    ? theme === 'neon'
                                        ? 'bg-neon-primary/30 text-accent'
                                        : 'bg-primary/10 text-primary'
                                    : theme === 'neon'
                                        ? 'hover:bg-neon-muted text-neon-text-primary'
                                        : 'hover:bg-aquatic-muted/30 text-aquatic-text-primary'
                                }
                `}
                            >
                                <span className="truncate max-w-[200px]">{option.label}</span>
                                <span
                                    className={`px-2 py-0.5 rounded text-xs font-medium ${getBadgeClass(option.type)}`}>
                  {option.level === 'project' ? 'Project' : option.type}
                </span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default FileSelector;