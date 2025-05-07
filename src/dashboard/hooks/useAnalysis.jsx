import {useState} from 'react';
import {analyzeFiles} from '../services/api';

/**
 * Custom hook for handling file analysis
 * @returns {Object} - Analysis methods and state
 */
const useAnalysis = () => {
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Run analysis on selected files
     * @param {FileList} files - The files to analyze
     * @returns {Promise<Object>} - Analysis result
     */
    const runAnalysis = async (files) => {
        try {
            setIsAnalyzing(true);
            setError(null);

            const result = await analyzeFiles(files);

            setIsAnalyzing(false);
            return result;
        } catch (err) {
            setError(err.message || 'Failed to analyze files');
            setIsAnalyzing(false);
            throw err;
        }
    };

    return {
        runAnalysis,
        isAnalyzing,
        error,
        setError
    };
};

export default useAnalysis;