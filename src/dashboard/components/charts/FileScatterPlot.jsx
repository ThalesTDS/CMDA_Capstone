import React, {useEffect, useRef, useState} from 'react';
import {useTheme} from '../../contexts/ThemeContext';
import Chart from 'chart.js/auto';
import {formatFileName} from '../../utils/utils';

const FileScatterPlot = ({files, maxFiles = 8}) => {
    const chartRef = useRef(null);
    const chartInstance = useRef(null);
    const {theme} = useTheme();
    const [selectedMetric, setSelectedMetric] = useState('accuracy');
    const metricOptions = ['accuracy', 'completeness', 'conciseness', 'comment_density', 'overall_score'];

    // Sort files by overall score in descending order and take maxFiles
    const limitedFiles = [...files]
        .sort((a, b) => b.overall_score - a.overall_score)
        .slice(0, maxFiles);

    const isTruncated = files.length > maxFiles;

    // Number labels for x-axis
    const numberLabels = limitedFiles.map((_, idx) => (idx + 1).toString());

    useEffect(() => {
        if (!chartRef.current || !limitedFiles.length) return;

        // Destroy previous chart if it exists
        if (chartInstance.current) {
            chartInstance.current.destroy();
        }

        const ctx = chartRef.current.getContext('2d');

        // Theme colors
        const colors = {
            human: theme === 'aquatic' ? 'rgba(0, 114, 181, 0.8)' : 'rgba(138, 43, 226, 0.8)',
            llm: theme === 'aquatic' ? 'rgba(0, 169, 206, 0.8)' : 'rgba(0, 255, 255, 0.8)',
            humanBorder: theme === 'aquatic' ? 'rgba(0, 114, 181, 1)' : 'rgba(138, 43, 226, 1)',
            llmBorder: theme === 'aquatic' ? 'rgba(0, 169, 206, 1)' : 'rgba(0, 255, 255, 1)',
            text: theme === 'aquatic' ? '#0A4D68' : '#E0E0FF',
            gridLines: theme === 'aquatic' ? 'rgba(0, 114, 181, 0.2)' : 'rgba(138, 43, 226, 0.2)',
        };

        // Set the max bubble size based on the largest line count
        const maxLineCount = Math.max(...limitedFiles.map(file => file.line_count));

        // Prepare datasets using number labels for x
        const datasets = [
            {
                label: 'Human',
                data: limitedFiles
                    .map((file, idx) => ({
                        x: (idx + 1).toString(),
                        y: (file.doc_type?.toLowerCase() || 'unknown') === 'human' ? (file[selectedMetric] || 0) : null,
                        r: Math.max(5, (file.line_count / maxLineCount) * 20),
                        fileIdx: idx
                    }))
                    .filter(d => d.y !== null),
                backgroundColor: colors.human,
                borderColor: colors.humanBorder,
                borderWidth: 1,
            },
            {
                label: 'LLM',
                data: limitedFiles
                    .map((file, idx) => ({
                        x: (idx + 1).toString(),
                        y: (file.doc_type?.toLowerCase() || 'unknown') === 'llm' ? (file[selectedMetric] || 0) : null,
                        r: Math.max(5, (file.line_count / maxLineCount) * 20),
                        fileIdx: idx
                    }))
                    .filter(d => d.y !== null),
                backgroundColor: colors.llm,
                borderColor: colors.llmBorder,
                borderWidth: 1,
            }
        ];

        chartInstance.current = new Chart(ctx, {
            type: 'bubble',
            data: {
                labels: numberLabels,
                datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'category',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: '', // No axis title, we'll add "File" label manually
                        },
                        ticks: {
                            color: colors.text,
                            callback: function(value, idx) {
                                return numberLabels[idx];
                            }
                        },
                        grid: {
                            color: colors.gridLines
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: selectedMetric.charAt(0).toUpperCase() + selectedMetric.slice(1).replace(/_/g, ' '),
                            color: colors.text,
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            color: colors.text
                        },
                        grid: {
                            color: colors.gridLines
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const idx = parseInt(context.raw.x, 10) - 1;
                                const file = limitedFiles[idx];
                                if (!file) return '';
                                const metricValue = file[selectedMetric]?.toFixed(2) ?? 'N/A';
                                const lineCount = file.line_count;
                                return [
                                    `${formatFileName(file.identifier)} (${file.doc_type})`,
                                    `${selectedMetric}: ${metricValue}`,
                                    `Line count: ${lineCount}`
                                ];
                            }
                        }
                    },
                    legend: {
                        labels: {
                            color: colors.text
                        }
                    },
                    title: {
                        display: true,
                        text: 'File Metrics Comparison',
                        color: colors.text,
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });

        return () => {
            if (chartInstance.current) {
                chartInstance.current.destroy();
            }
        };
    }, [limitedFiles, selectedMetric, theme]);

    return (
        <div className="w-full flex flex-row">
            {/* Left axis label */}
            <div className="flex flex-col items-center mr-2 mt-16">
                <span className="text-xs font-semibold rotate-[-45deg] text-gray-500" style={{writingMode: 'vertical-lr', transform: 'rotate(-90deg)'}}>File</span>
            </div>
            <div className="flex-1">
                <div className="flex justify-end mb-4">
                    <div className="flex items-center">
                        <label className="mr-2 text-sm font-medium">Metric:</label>
                        <select
                            value={selectedMetric}
                            onChange={(e) => setSelectedMetric(e.target.value)}
                            className={`
                  text-sm rounded-md border px-3 py-1.5 
                  ${theme === 'neon'
                                    ? 'bg-neon-surface border-neon-border text-neon-text-primary'
                                    : 'bg-white border-primary/20 text-aquatic-text-primary'
                                }
                `}
                        >
                            {metricOptions.map(metric => (
                                <option key={metric} value={metric}>
                                    {metric.charAt(0).toUpperCase() + metric.slice(1).replace(/_/g, ' ')}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="h-80">
                    <canvas ref={chartRef}></canvas>
                </div>

                {isTruncated && (
                    <div className="mt-2 text-center text-sm text-muted-foreground">
                        Note: Only showing top {maxFiles} files by overall score. {files.length - maxFiles} additional files
                        are not displayed.
                    </div>
                )}
            </div>
            {/* File legend */}
            <div className="ml-6 flex flex-col items-start justify-start mt-8">
                <div className="font-semibold mb-2">Files</div>
                <ul className="text-xs">
                    {limitedFiles.map((file, idx) => (
                        <li key={file.identifier} className="mb-1">
                            <span className="font-bold">{idx + 1}.</span> {formatFileName(file.identifier)}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default FileScatterPlot;
