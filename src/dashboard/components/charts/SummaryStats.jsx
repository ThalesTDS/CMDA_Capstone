import React from 'react';
import {findBestAndWorstMetrics, formatMetricValue} from '../../utils/utils';
import {useTheme} from '../../contexts/ThemeContext';

const SummaryStats = ({metrics}) => {
    const {theme} = useTheme();

    if (!metrics) return null;

    const {bestMetric, worstMetric} = findBestAndWorstMetrics(metrics);

    // Format metric name for display
    const formatMetricName = (name) => {
        return name
            .replace(/_/g, ' ')
            .replace(/\b\w/g, (l) => l.toUpperCase());
    };

    // Get color class based on value
    const getColorClass = (value) => {
        if (value < 0.33) return theme === 'neon' ? 'text-red-400' : 'text-red-500';
        if (value < 0.66) return theme === 'neon' ? 'text-yellow-300' : 'text-yellow-500';
        return theme === 'neon' ? 'text-green-300' : 'text-green-500';
    };

    // Get badge color
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

    const statCardClasses = `bg-card ${theme === 'neon' ? 'shadow-[0_4px_12px_rgba(0,0,0,0.5)] border border-neon-border/50' : 'shadow-md border border-primary/10'} rounded-xl p-4 transition-all duration-300 hover:scale-[1.02] hover-scale`;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className={statCardClasses}>
                <div className="flex justify-between items-start mb-4">
                    <h3 className={`text-lg font-semibold ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>
                        Best Metric
                    </h3>

                    <div className={`flex items-center ${getColorClass(bestMetric.value)}`}>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20"
                             fill="currentColor">
                            <path fillRule="evenodd"
                                  d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
                                  clipRule="evenodd"/>
                        </svg>
                        <span className="font-bold text-lg">
              {formatMetricValue(bestMetric.value)}
            </span>
                    </div>
                </div>

                <div className={`text-xl font-bold mb-2 ${theme === 'neon' ? 'text-foreground' : ''}`}>
                    {formatMetricName(bestMetric.name)}
                </div>

                <div className="w-full bg-muted rounded-full h-2.5 mt-4">
                    <div
                        className={`h-2.5 rounded-full progress-bar-animated ${theme === 'neon' ? 'bg-accent' : 'bg-primary'}`}
                        style={{width: `${bestMetric.value * 100}%`}}
                    ></div>
                </div>
            </div>

            <div className={statCardClasses}>
                <div className="flex justify-between items-start mb-4">
                    <h3 className={`text-lg font-semibold ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>
                        Worst Metric
                    </h3>

                    <div className={`flex items-center ${getColorClass(worstMetric.value)}`}>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20"
                             fill="currentColor">
                            <path fillRule="evenodd"
                                  d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
                                  clipRule="evenodd"/>
                        </svg>
                        <span className="font-bold text-lg">
              {formatMetricValue(worstMetric.value)}
            </span>
                    </div>
                </div>

                <div className={`text-xl font-bold mb-2 ${theme === 'neon' ? 'text-foreground' : ''}`}>
                    {formatMetricName(worstMetric.name)}
                </div>

                <div className="w-full bg-muted rounded-full h-2.5 mt-4">
                    <div
                        className={`h-2.5 rounded-full progress-bar-animated ${theme === 'neon' ? 'bg-accent/50' : 'bg-primary/50'}`}
                        style={{width: `${worstMetric.value * 100}%`}}
                    ></div>
                </div>
            </div>

            <div className={statCardClasses}>
                <div className="flex justify-between items-start mb-6">
                    <h3 className={`text-lg font-semibold ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>
                        Overall Score
                    </h3>
                </div>

                <div className="flex items-center justify-center">
                    <div className={`text-6xl font-bold relative ${getColorClass(metrics.overall_score)}`}>
                        {formatMetricValue(metrics.overall_score)}
                        <span
                            className={`absolute bottom-1 -right-4 text-xs font-normal ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>
              /1.0
            </span>
                    </div>
                </div>
            </div>

            <div className={statCardClasses}>
                <div className="flex justify-between items-start mb-4">
                    <h3 className={`text-lg font-semibold ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}>
                        File Info
                    </h3>

                    <div
                        className={`px-2.5 py-0.5 rounded text-xs font-medium ${getBadgeClass(metrics.doc_type)}`}
                    >
                        {metrics.doc_type}
                    </div>
                </div>

                <div className="space-y-3">
                    <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">File Name:</span>
                        <span className="text-sm font-medium truncate max-w-[200px]">
              {metrics.identifier.split('/').pop()}
            </span>
                    </div>

                    <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">Line Count:</span>
                        <div className="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg"
                                 className={`h-4 w-4 mr-1 ${theme === 'neon' ? 'text-accent' : 'text-primary'}`}
                                 viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                                <path fillRule="evenodd"
                                      d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                                      clipRule="evenodd"/>
                            </svg>
                            <span className="text-sm font-medium">{metrics.line_count}</span>
                        </div>
                    </div>

                    <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">Level:</span>
                        <span className="text-sm font-medium capitalize">{metrics.level}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SummaryStats;