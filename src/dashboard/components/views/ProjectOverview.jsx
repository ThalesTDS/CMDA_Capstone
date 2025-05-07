import React, {useEffect, useRef} from 'react';
import {useMetrics} from '../../contexts/MetricsContext';
import {useTheme} from '../../contexts/ThemeContext';
import Chart from 'chart.js/auto';
import FileScatterPlot from '../charts/FileScatterPlot';

const ProjectOverview = () => {
    const {getProjectMetrics, metricsData} = useMetrics();
    const {theme} = useTheme();
    const barChartRef = useRef(null);
    const barChartInstance = useRef(null);

    const projectMetrics = getProjectMetrics();

    if (!projectMetrics || !metricsData) {
        return (
            <div className="p-6 text-center">
                <p className="text-muted-foreground">Project metrics not available</p>
            </div>
        );
    }

    // Get theme colors
    const getThemeColors = () => {
        return {
            primary: theme === 'aquatic' ? '#0072B5' : '#8A2BE2',
            secondary: theme === 'aquatic' ? '#00A9CE' : '#FF00FF',
            accent: theme === 'aquatic' ? '#38B0DE' : '#00FFFF',
            text: theme === 'aquatic' ? '#0A4D68' : '#E0E0FF',
            background: theme === 'aquatic' ? '#FFFFFF' : '#1A1A3A',
        };
    };

    // Create bar chart for average metrics
    useEffect(() => {
        if (!barChartRef.current || !metricsData.file.length) return;

        // Destroy previous chart if it exists
        if (barChartInstance.current) {
            barChartInstance.current.destroy();
        }

        const ctx = barChartRef.current.getContext('2d');
        const colors = getThemeColors();

        // Group files by doc type
        const docTypes = [...new Set(metricsData.file.map(file => file.doc_type))];
        const metricKeys = ['comment_density', 'completeness', 'conciseness', 'accuracy', 'overall_score'];

        // Calculate average metrics by doc type
        const docTypeMetrics = docTypes.map(type => {
            const typedFiles = metricsData.file.filter(file => file.doc_type === type);

            return {
                docType: type,
                metrics: metricKeys.reduce((acc, metric) => {
                    acc[metric] = typedFiles.reduce((sum, file) => sum + file[metric], 0) / typedFiles.length;
                    return acc;
                }, {})
            };
        });

        // Prepare data for the chart
        const datasets = docTypes.map((type, index) => {
            const typeData = docTypeMetrics.find(data => data.docType === type);
            return {
                label: type,
                data: metricKeys.map(key => typeData.metrics[key]),
                backgroundColor: [colors.primary, colors.secondary, colors.accent][index % 3] + '80',
                borderColor: [colors.primary, colors.secondary, colors.accent][index % 3],
                borderWidth: 1
            };
        });

        // Create the chart
        barChartInstance.current = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: metricKeys.map(key =>
                    key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                ),
                datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            color: colors.text
                        },
                        grid: {
                            color: colors.text + '20'
                        }
                    },
                    x: {
                        ticks: {
                            color: colors.text
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Average Metric Scores by Documentation Type',
                        color: colors.text,
                        font: {
                            size: 16,
                            weight: 'bold',
                        },
                        padding: {
                            top: 10,
                            bottom: 10
                        }
                    },
                    legend: {
                        display: true,
                        labels: {
                            color: colors.text
                        }
                    },
                    tooltip: {
                        backgroundColor: theme === 'aquatic' ? 'rgba(255, 255, 255, 0.9)' : 'rgba(26, 26, 58, 0.9)',
                        titleColor: colors.text,
                        bodyColor: colors.text,
                        borderColor: colors.primary,
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            label: (context) => {
                                return `${context.dataset.label}: ${context.raw.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });

        // Cleanup
        return () => {
            if (barChartInstance.current) {
                barChartInstance.current.destroy();
            }
        };
    }, [metricsData, theme]);

    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-6">Project Overview</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="card">
                    <h3 className="text-lg font-semibold mb-2">Project Summary</h3>
                    <div className="grid grid-cols-2 gap-4 mt-4">
                        <div>
                            <p className="text-sm text-muted-foreground">Total Files</p>
                            <p className="text-xl font-bold">{projectMetrics.num_files || metricsData.file.length}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Total Lines</p>
                            <p className="text-xl font-bold">{projectMetrics.line_count}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Overall Score</p>
                            <p className="text-xl font-bold">{projectMetrics.overall_score.toFixed(2)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Documentation Type</p>
                            <p className="text-xl font-bold">{projectMetrics.doc_type}</p>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h3 className="text-lg font-semibold mb-2">Metric Highlights</h3>
                    <div className="space-y-4 mt-4">
                        {['comment_density', 'completeness', 'conciseness', 'accuracy'].map(metric => (
                            <div key={metric} className="flex items-center justify-between">
                <span className="text-sm">
                  {metric.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
                                <div className="w-2/3 bg-muted rounded-full h-2.5">
                                    <div
                                        className="h-2.5 rounded-full bg-primary"
                                        style={{width: `${projectMetrics[metric] * 100}%`}}
                                    ></div>
                                </div>
                                <span className="text-sm font-medium w-12 text-right">
                  {(projectMetrics[metric] * 100).toFixed(1)}%
                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="card">
                <h3 className="text-lg font-semibold mb-4">Metrics by Documentation Type</h3>
                <div className="h-72">
                    <canvas ref={barChartRef}></canvas>
                </div>
            </div>

            {/* Show scatter plot if there are multiple files */}
            {metricsData.file.length > 1 && (
                <div className="card mt-6">
                    <h3 className="text-lg font-semibold mb-4">Files Comparison</h3>
                    <FileScatterPlot files={metricsData.file} maxFiles={8}/>
                </div>
            )}
        </div>
    );
};

export default ProjectOverview;