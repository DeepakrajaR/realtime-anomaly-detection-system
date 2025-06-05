import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { ChartData } from '../../types';

interface RealtimeChartProps {
  data: ChartData[];
  width?: number;
  height?: number;
  margin?: { top: number; right: number; bottom: number; left: number };
  maxPoints?: number;
}

const RealtimeChart: React.FC<RealtimeChartProps> = ({
  data,
  width = 800,
  height = 400,
  margin = { top: 20, right: 30, bottom: 30, left: 40 },
  maxPoints = 100,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width, height });

  useEffect(() => {
    // Update dimensions on resize
    const handleResize = () => {
      if (svgRef.current) {
        const newWidth = svgRef.current.parentElement?.clientWidth || width;
        setDimensions({
          width: newWidth,
          height,
        });
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [height, width]);

  useEffect(() => {
    if (!svgRef.current || data.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous chart

    // Calculate inner dimensions
    const innerWidth = dimensions.width - margin.left - margin.right;
    const innerHeight = dimensions.height - margin.top - margin.bottom;

    // Create scales
    const xScale = d3
      .scaleLinear()
      .domain([0, Math.max(maxPoints, data.length)])
      .range([0, innerWidth]);

    const yDomain = d3.extent(data, (d) => d.value) as [number, number];
    const yPadding = (yDomain[1] - yDomain[0]) * 0.1;
    
    const yScale = d3
      .scaleLinear()
      .domain([yDomain[0] - yPadding, yDomain[1] + yPadding])
      .range([innerHeight, 0]);

    // Create a line generator
    const line = d3
      .line<ChartData>()
      .x((d, i) => xScale(i))
      .y((d) => yScale(d.value))
      .curve(d3.curveMonotoneX);

    // Create the container group
    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add axes
    g.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale));

    g.append('g')
      .attr('class', 'y-axis')
      .call(d3.axisLeft(yScale));

    // Add line path
    g.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#3b82f6')
      .attr('stroke-width', 1.5)
      .attr('d', line);

    // Add data points
    g.selectAll('.data-point')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', (d) => (d.is_anomaly ? 'anomaly' : 'normal'))
      .attr('cx', (d, i) => xScale(i))
      .attr('cy', (d) => yScale(d.value))
      .attr('r', (d) => (d.is_anomaly ? 5 : 3))
      .attr('fill', (d) => (d.is_anomaly ? '#ef4444' : '#3b82f6'))
      .on('mouseover', function (event, d) {
        // Show tooltip
        const tooltip = d3.select(tooltipRef.current);
        tooltip
          .style('opacity', 1)
          .style('left', `${event.pageX + 10}px`)
          .style('top', `${event.pageY - 20}px`)
          .html(`
            <div>
              <div>Value: ${d.value.toFixed(3)}</div>
              <div>Time: ${new Date(d.timestamp).toLocaleTimeString()}</div>
              <div>Type: ${d.is_anomaly ? 'Anomaly' : 'Normal'}</div>
            </div>
          `);
        
        // Highlight the point
        d3.select(this)
          .attr('r', d.is_anomaly ? 7 : 5)
          .attr('stroke', '#000')
          .attr('stroke-width', 2);
      })
      .on('mouseout', function (event, d) {
        // Hide tooltip
        d3.select(tooltipRef.current).style('opacity', 0);
        
        // Reset point styling
        d3.select(this)
          .attr('r', d.is_anomaly ? 5 : 3)
          .attr('stroke', d.is_anomaly ? '#ef4444' : '#3b82f6')
          .attr('stroke-width', 1);
      });

    // Add grid lines
    g.append('g')
      .attr('class', 'grid')
      .attr('opacity', 0.1)
      .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(() => ''));

  }, [data, dimensions, margin, maxPoints]);

  return (
    <div className="chart-container">
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="w-full h-full"
      />
      <div
        ref={tooltipRef}
        className="tooltip"
        style={{ opacity: 0 }}
      />
    </div>
  );
};

export default RealtimeChart;