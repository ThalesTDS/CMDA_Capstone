import React, {useEffect, useRef} from 'react';
import {formatMetricValue} from '../../utils/utils';
import {useTheme} from '../../contexts/ThemeContext';

const GaugeChart = ({metric, value, size = 180}) => {
    const canvasRef = useRef(null);
    const animationRef = useRef(null);
    const currentValueRef = useRef(0);
    const {theme} = useTheme();

    // Format the metric name for display
    const formatMetricName = (name) => {
        return name
            .replace(/_/g, ' ')
            .replace(/\b\w/g, (l) => l.toUpperCase());
    };

    // Get color based on value
    const getColor = (val) => {
        if (theme === 'aquatic') {
            // Aquatic theme colors
            if (val < 0.33) return '#EF4444';
            if (val < 0.66) return '#F59E0B';
            return '#10B981';
        } else {
            // Neon theme colors
            if (val < 0.33) return '#FF3B5C';
            if (val < 0.66) return '#FFAA33';
            return '#36EFB1';
        }
    };

    // Get glow style based on theme
    const getGlowStyle = (color) => {
        if (theme === 'neon') {
            return `0 0 10px ${color}80, 0 0 15px ${color}40`;
        }
        return 'none';
    };

    // Animate the gauge to the target value
    const animateGauge = (targetValue) => {
        // Start from current value
        const startValue = currentValueRef.current;
        const startTime = Date.now();
        const duration = 1500; // Animation duration in ms

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function for smooth animation
            const easeOutCubic = (x) => 1 - Math.pow(1 - x, 3);
            const easedProgress = easeOutCubic(progress);

            // Calculate current animated value
            currentValueRef.current = startValue + (targetValue - startValue) * easedProgress;

            // Draw the gauge
            drawGauge(currentValueRef.current);

            // Continue animation if not complete
            if (progress < 1) {
                animationRef.current = requestAnimationFrame(animate);
            }
        };

        // Cancel any existing animation
        if (animationRef.current) {
            cancelAnimationFrame(animationRef.current);
        }

        // Start animation
        animationRef.current = requestAnimationFrame(animate);
    };

    // Draw the gauge
    const drawGauge = (currentValue) => {
        if (!canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) * 0.8;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw outer ring (background track)
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, Math.PI, 2 * Math.PI, false);
        ctx.lineWidth = theme === 'neon' ? 10 : 15;
        ctx.strokeStyle = theme === 'neon' ? '#1A1A3A' : '#E5E7EB';
        ctx.stroke();

        // Draw value arc
        const endAngle = Math.PI + (currentValue * Math.PI);
        const valueColor = getColor(currentValue);

        // Gradient fill for the gauge
        const gradient = ctx.createLinearGradient(0, centerY - radius, 0, centerY + radius);
        if (theme === 'neon') {
            gradient.addColorStop(0, valueColor + '80');
            gradient.addColorStop(1, valueColor);
        } else {
            gradient.addColorStop(0, valueColor);
            gradient.addColorStop(1, valueColor + '90');
        }

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, Math.PI, endAngle, false);
        ctx.lineWidth = theme === 'neon' ? 10 : 15;
        ctx.strokeStyle = gradient;

        // Add glow effect for neon theme
        if (theme === 'neon') {
            ctx.shadowColor = valueColor;
            ctx.shadowBlur = 10;
        }

        ctx.stroke();

        // Reset shadow
        ctx.shadowBlur = 0;

        // Draw center circle with gradient
        const centerGradient = ctx.createRadialGradient(
            centerX, centerY, 0,
            centerX, centerY, radius * 0.7
        );

        if (theme === 'neon') {
            centerGradient.addColorStop(0, '#2D2D5F');
            centerGradient.addColorStop(1, '#1A1A3A');
        } else {
            centerGradient.addColorStop(0, '#FFFFFF');
            centerGradient.addColorStop(1, '#F7FAFC');
        }

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.7, 0, 2 * Math.PI, false);
        ctx.fillStyle = centerGradient;
        ctx.fill();

        // Draw ticks
        for (let i = 0; i <= 10; i++) {
            const angle = Math.PI + (i / 10) * Math.PI;
            const tickLength = i % 5 === 0 ? 10 : 5;

            const startX = centerX + (radius - tickLength) * Math.cos(angle);
            const startY = centerY + (radius - tickLength) * Math.sin(angle);
            const endX = centerX + radius * Math.cos(angle);
            const endY = centerY + radius * Math.sin(angle);

            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.lineWidth = i % 5 === 0 ? 2 : 1;
            ctx.strokeStyle = theme === 'neon' ? '#6E6E9E' : '#CBD5E0';
            ctx.stroke();
        }

        // Draw value text
        ctx.font = `bold ${radius * 0.25}px Inter, sans-serif`;
        ctx.fillStyle = theme === 'neon' ? '#E0E0FF' : getColor(currentValue);
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Add small glow to text for neon theme
        if (theme === 'neon') {
            ctx.shadowColor = valueColor;
            ctx.shadowBlur = 5;
        }

        ctx.fillText(formatMetricValue(currentValue), centerX, centerY - 10);

        // Reset shadow
        ctx.shadowBlur = 0;

        // Draw label
        ctx.font = `${radius * 0.12}px Inter, sans-serif`;
        ctx.fillStyle = theme === 'neon' ? '#9D9DCB' : '#6B7280';
        ctx.fillText(formatMetricName(metric), centerX, centerY + radius * 0.2);

        // Draw min/max labels
        ctx.font = `${radius * 0.1}px Inter, sans-serif`;
        ctx.fillStyle = theme === 'neon' ? '#6E6E9E' : '#94A3B8';
        ctx.textAlign = 'left';
        ctx.fillText('0', centerX - radius * 0.9, centerY + radius * 0.4);
        ctx.textAlign = 'right';
        ctx.fillText('1', centerX + radius * 0.9, centerY + radius * 0.4);
    };

    // Initialize and animate gauge when mounted or value changes
    useEffect(() => {
        if (canvasRef.current) {
            // Set up canvas with correct DPI
            const canvas = canvasRef.current;
            const dpr = window.devicePixelRatio || 1;
            canvas.width = size * dpr;
            canvas.height = (size / 1.5) * dpr;
            const ctx = canvas.getContext('2d');
            ctx.scale(dpr, dpr);
            canvas.style.width = `${size}px`;
            canvas.style.height = `${size / 1.5}px`;

            // Animate to the new value
            animateGauge(value);
        }

        // Clean up animation on unmount or update
        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [value, size, theme]);

    return (
        <div
            className="relative"
            style={{
                width: `${size}px`,
                height: `${size / 1.5 + 16}px`, // add space for bar
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'flex-start',
            }}
        >
            {/* Gauge Canvas */}
            <div
                style={{
                    width: `${size}px`,
                    height: `${size / 1.5}px`,
                    display: 'flex',
                    alignItems: 'flex-start',
                    justifyContent: 'center',
                    position: 'absolute',
                    top: 0,
                    left: '-25px', // <-- Offset to the left for better centering
                    right: 0,
                    pointerEvents: 'none', // prevent accidental offset
                }}
            >
                <canvas
                    ref={canvasRef}
                    style={{
                        display: 'block',
                        margin: '0 auto',
                        width: `${size}px`,
                        height: `${size / 1.5}px`,
                    }}
                    width={size}
                    height={size / 1.5}
                    className={theme === 'neon' ? 'gauge-neon' : ''}
                />
            </div>
            {/* Bar */}
            <div
                style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    width: `${size}px`,
                    height: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    zIndex: 2,
                }}
                className={`w-full rounded-full overflow-hidden ${theme === 'neon' ? 'bg-background' : 'bg-muted'}`}
            >
                <div
                    className={`h-full ${theme === 'neon' ? 'bg-accent' : 'bg-primary'} rounded-full transition-all duration-1000 progress-bar-animated`}
                    style={{width: `${value * 100}%`}}
                ></div>
            </div>
        </div>
    );
};

export default GaugeChart;