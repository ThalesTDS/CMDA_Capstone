/**
 * Format a metric value for display
 * @param {number} value - The metric value (0-1)
 * @param {boolean} asPercentage - Whether to display as percentage
 * @returns {string} - Formatted metric value
 */
export const formatMetricValue = (value, asPercentage = false) => {
    if (value === undefined || value === null) return 'N/A';

    if (asPercentage) {
        return `${(value * 100).toFixed(1)}%`;
    }

    return value.toFixed(2);
};

/**
 * Get color based on metric value
 * @param {number} value - The metric value (0-1)
 * @returns {string} - Color class name
 */
export const getMetricColor = (value) => {
    if (value === undefined || value === null) return 'text-muted-foreground';

    if (value < 0.33) return 'text-red-500';
    if (value < 0.66) return 'text-yellow-500';
    return 'text-green-500';
};

/**
 * Get color for chart based on index
 * @param {number} index - The index
 * @returns {string} - CSS variable for chart color
 */
export const getChartColor = (index) => {
    return `var(--chart-color-${(index % 5) + 1})`;
};

/**
 * Format file name for display (extract base name)
 * @param {string} filePath - The file path
 * @returns {string} - Base file name
 */
export const formatFileName = (filePath) => {
    if (!filePath) return '';

    return filePath.split('/').pop();
};

/**
 * Parse CSV data into an array of objects
 * @param {string} csvText - The CSV text content
 * @returns {Array} - Array of objects representing CSV rows
 */
export const parseCSV = (csvText) => {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');

    return lines.slice(1).map(line => {
        const values = line.split(',');
        const obj = {};

        headers.forEach((header, i) => {
            // Convert numeric values
            const value = values[i] || '';
            obj[header] = !isNaN(value) && value !== '' ? parseFloat(value) : value;
        });

        return obj;
    });
};

/**
 * Group metrics data by level (file or project)
 * @param {Array} metricsData - Array of metrics objects
 * @returns {Object} - Grouped metrics by level
 */
export const groupMetricsByLevel = (metricsData) => {
    const result = {
        file: [],
        project: []
    };

    metricsData.forEach(metric => {
        if (metric.level === 'file') {
            result.file.push(metric);
        } else if (metric.level === 'project') {
            result.project.push(metric);
        }
    });

    return result;
};

/**
 * Find the best and worst metrics for a file
 * @param {Object} fileMetrics - Metrics for a single file
 * @returns {Object} - Best and worst metrics
 */
export const findBestAndWorstMetrics = (fileMetrics) => {
    const metricKeys = ['comment_density', 'completeness', 'conciseness', 'accuracy'];
    let bestMetric = {name: '', value: 0};
    let worstMetric = {name: '', value: 1};

    metricKeys.forEach(metric => {
        const value = fileMetrics[metric];

        if (value > bestMetric.value) {
            bestMetric = {name: metric, value};
        }

        if (value < worstMetric.value) {
            worstMetric = {name: metric, value};
        }
    });

    return {bestMetric, worstMetric};
};