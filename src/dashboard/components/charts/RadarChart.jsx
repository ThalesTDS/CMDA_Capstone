import React, { useEffect, useRef, useState } from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const RadarChart = ({ data, title = 'Metrics Radar Chart' }) => {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const animationRef = useRef(null);
  const [isHovering, setIsHovering] = useState(false);
  const [activeMetric, setActiveMetric] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [animationProgress, setAnimationProgress] = useState(0);
  const { theme } = useTheme();
  
  // Animate radar chart on mount
  useEffect(() => {
    const startTime = Date.now();
    const duration = 1500; // Animation duration in ms
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function for smooth animation
      const easeOutCubic = (x) => 1 - Math.pow(1 - x, 3);
      const easedProgress = easeOutCubic(progress);
      
      setAnimationProgress(easedProgress);
      
      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };
    
    animationRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [data]);
  
  // Draw radar chart when data or theme changes
  useEffect(() => {
    if (!svgRef.current || !data) return;
    
    const metricKeys = ['comment_density', 'completeness', 'conciseness', 'accuracy'];
    const metricLabels = metricKeys.map(key => 
      key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    );
    
    // Get values from data
    const metricValues = metricKeys.map(key => data[key] || 0);
    
    // Calculate dimensions
    const svg = svgRef.current;
    const rect = svg.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) * 0.7 * animationProgress;
    
    // Clear SVG
    while (svg.firstChild) {
      svg.removeChild(svg.firstChild);
    }
    
    // Create a group for the chart
    const chart = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    chart.setAttribute('transform', `translate(${centerX}, ${centerY})`);
    svg.appendChild(chart);
    
    // Theme colors
    const primaryColor = theme === 'aquatic' ? '#0072B5' : '#8A2BE2';
    const accentColor = theme === 'aquatic' ? '#38B0DE' : '#00FFFF';
    const mutedColor = theme === 'aquatic' ? '#D0E6F5' : '#4B0082';
    const textColor = theme === 'aquatic' ? '#0A4D68' : '#E0E0FF';
    const textSecondary = theme === 'aquatic' ? '#498BA6' : '#BC9DFF';
    
    // Draw circles with higher contrast
    for (let i = 5; i > 0; i--) {
      const circleRadius = radius * (i / 5);
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', 0);
      circle.setAttribute('cy', 0);
      circle.setAttribute('r', circleRadius);
      circle.setAttribute('fill', 'none');
      circle.setAttribute('stroke', mutedColor);
      circle.setAttribute('stroke-opacity', theme === 'aquatic' ? 0.6 : 0.5); // Increased contrast
      circle.setAttribute('stroke-width', theme === 'neon' ? '1.5' : '1'); // Thicker lines
      circle.setAttribute('stroke-dasharray', theme === 'neon' ? '3,3' : '1,1');
      chart.appendChild(circle);
      
      // Add tick labels (0.2, 0.4, 0.6, 0.8, 1.0)
      const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', 5);
      label.setAttribute('y', -circleRadius + 15);
      label.setAttribute('fill', textSecondary);
      label.setAttribute('font-size', '10');
      label.textContent = (i / 5).toFixed(1);
      chart.appendChild(label);
    }
    
    // Draw axes
    metricLabels.forEach((label, i) => {
      const angle = (Math.PI * 2 * i) / metricLabels.length - Math.PI / 2;
      const x = radius * Math.cos(angle);
      const y = radius * Math.sin(angle);
      
      // Draw axis with higher contrast
      const axis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      axis.setAttribute('x1', 0);
      axis.setAttribute('y1', 0);
      axis.setAttribute('x2', x);
      axis.setAttribute('y2', y);
      axis.setAttribute('stroke', mutedColor);
      axis.setAttribute('stroke-opacity', theme === 'aquatic' ? 0.6 : 0.5); // Increased contrast
      axis.setAttribute('stroke-width', '1.2'); // Thicker lines
      chart.appendChild(axis);
      
      // Add label
      const labelEl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      const labelX = x * 1.2;
      const labelY = y * 1.2;
      labelEl.setAttribute('x', labelX);
      labelEl.setAttribute('y', labelY);
      labelEl.setAttribute('text-anchor', labelX < 0 ? 'end' : labelX === 0 ? 'middle' : 'start');
      labelEl.setAttribute('dominant-baseline', labelY < 0 ? 'auto' : labelY === 0 ? 'middle' : 'hanging');
      labelEl.setAttribute('fill', textColor);
      labelEl.setAttribute('font-size', '12');
      labelEl.setAttribute('font-weight', activeMetric === metricKeys[i] ? 'bold' : 'normal');
      labelEl.classList.add('radar-label');
      labelEl.setAttribute('data-metric', metricKeys[i]);
      labelEl.textContent = label;
      
      // Add hover effect for labels
      labelEl.addEventListener('mouseover', () => {
        setActiveMetric(metricKeys[i]);
        const rect = labelEl.getBoundingClientRect();
        const containerRect = containerRef.current.getBoundingClientRect();
        setTooltipPosition({
          x: rect.left + rect.width / 2 - containerRect.left,
          y: rect.top - containerRect.top
        });
        setIsHovering(true);
      });
      
      labelEl.addEventListener('mouseout', () => {
        setActiveMetric(null);
        setIsHovering(false);
      });
      
      chart.appendChild(labelEl);
    });
    
    // Calculate points for polygon
    const points = metricValues.map((value, i) => {
      const angle = (Math.PI * 2 * i) / metricValues.length - Math.PI / 2;
      const distance = value * radius * animationProgress;
      const x = distance * Math.cos(angle);
      const y = distance * Math.sin(angle);
      return { x, y, value };
    });

    const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    polygon.setAttribute('points', points.map(p => `${p.x},${p.y}`).join(' '));
    polygon.setAttribute('fill', primaryColor);
    polygon.setAttribute('fill-opacity', theme === 'aquatic' ? 0.2 : 0.3);
    polygon.setAttribute('stroke', primaryColor);
    polygon.setAttribute('stroke-width', '2');
    
    // Add subtle pulse animation instead of rotation to keep polygon properly aligned
    const pulseAnimation = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
    pulseAnimation.setAttribute('attributeName', 'fill-opacity');
    pulseAnimation.setAttribute('values', theme === 'aquatic' ? '0.2;0.3;0.2' : '0.3;0.4;0.3');
    pulseAnimation.setAttribute('dur', '3s');
    pulseAnimation.setAttribute('repeatCount', 'indefinite');
    polygon.appendChild(pulseAnimation);
    
    chart.appendChild(polygon);
    
    // Add data points
    points.forEach((point, i) => {
      const pointGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      chart.appendChild(pointGroup);
      
      // Draw point shadow/glow
      if (theme === 'neon') {
        const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        glow.setAttribute('cx', point.x);
        glow.setAttribute('cy', point.y);
        glow.setAttribute('r', '6');
        glow.setAttribute('fill', accentColor);
        glow.setAttribute('opacity', '0.3');
        glow.setAttribute('class', activeMetric === metricKeys[i] ? 'radar-point' : '');
        pointGroup.appendChild(glow);
      }
      
      // Draw point
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', point.x);
      circle.setAttribute('cy', point.y);
      circle.setAttribute('r', '4');
      circle.setAttribute('fill', theme === 'neon' ? accentColor : primaryColor);
      circle.setAttribute('stroke', 'white');
      circle.setAttribute('stroke-width', '1');
      
      // Add hover events
      circle.addEventListener('mouseover', (e) => {
        setActiveMetric(metricKeys[i]);
        const rect = circle.getBoundingClientRect();
        const containerRect = containerRef.current.getBoundingClientRect();
        setTooltipPosition({
          x: rect.left + rect.width / 2 - containerRect.left,
          y: rect.top - containerRect.top
        });
        setIsHovering(true);
      });
      
      circle.addEventListener('mouseout', () => {
        setActiveMetric(null);
        setIsHovering(false);
      });
      
      pointGroup.appendChild(circle);
      
      // Show value if this is the active metric
      if (activeMetric === metricKeys[i]) {
        const valueLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        valueLabel.setAttribute('x', point.x);
        valueLabel.setAttribute('y', point.y - 10);
        valueLabel.setAttribute('text-anchor', 'middle');
        valueLabel.setAttribute('fill', theme === 'neon' ? accentColor : primaryColor);
        valueLabel.setAttribute('font-size', '12');
        valueLabel.setAttribute('font-weight', 'bold');
        valueLabel.textContent = point.value.toFixed(2);
        pointGroup.appendChild(valueLabel);
      }
    });
    
    // Add title
    const titleElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    titleElement.setAttribute('x', 0);
    titleElement.setAttribute('y', -height / 2 + 20);
    titleElement.setAttribute('text-anchor', 'middle');
    titleElement.setAttribute('fill', textColor);
    titleElement.setAttribute('font-size', '16');
    titleElement.setAttribute('font-weight', 'bold');
    titleElement.textContent = title;
    chart.appendChild(titleElement);
    
  }, [data, theme, animationProgress, activeMetric, isHovering]);
  
  return (
    <div ref={containerRef} className="relative h-64 w-full">
      <svg ref={svgRef} width="100%" height="100%" className="overflow-visible"></svg>
      
      {isHovering && activeMetric && (
        <div 
          className={`absolute px-3 py-2 rounded-md text-xs font-medium ${
            theme === 'neon'
              ? 'bg-neon-surface/90 text-neon-text-primary border border-neon-border shadow-[0_0_10px_rgba(138,43,226,0.3)]'
              : 'bg-white/90 text-aquatic-text-primary border border-aquatic-border shadow-md'
          } transform -translate-x-1/2 -translate-y-full z-10 transition-opacity duration-200`}
          style={{ 
            left: tooltipPosition.x,
            top: tooltipPosition.y - 10
          }}
        >
          <div className="font-bold">{activeMetric.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
          <div>Value: {(data[activeMetric] || 0).toFixed(2)}</div>
        </div>
      )}
    </div>
  );
};

export default RadarChart;