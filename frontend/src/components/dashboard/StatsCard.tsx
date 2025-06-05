import React from 'react';
import { ChartData, AnomalyDetection } from '../../types';

interface StatsCardProps {
  data: ChartData[];
  anomalies: AnomalyDetection[];
}

const StatsCard: React.FC<StatsCardProps> = ({ data, anomalies }) => {
  // Calculate statistics
  const totalDataPoints = data.length;
  const totalAnomalies = anomalies.length;
  const anomalyPercentage = totalDataPoints > 0 
    ? ((totalAnomalies / totalDataPoints) * 100).toFixed(2)
    : '0.00';
    
  const latestValue = data.length > 0 
    ? data[data.length - 1].value.toFixed(3)
    : 'N/A';
    
  const recentValues = data.slice(-10);
  const avgValue = recentValues.length > 0
    ? (recentValues.reduce((sum, point) => sum + point.value, 0) / recentValues.length).toFixed(3)
    : 'N/A';

  return (
    <div className="grid grid-4 mb-6">
      <div className="card">
        <div className="stats-label">Total Data Points</div>
        <div className="stats-value">{totalDataPoints}</div>
      </div>
      
      <div className="card">
        <div className="stats-label">Anomalies Detected</div>
        <div className="stats-value text-danger">{totalAnomalies}</div>
        <div className="stats-subtext">({anomalyPercentage}% of total)</div>
      </div>
      
      <div className="card">
        <div className="stats-label">Latest Value</div>
        <div className="stats-value">{latestValue}</div>
      </div>
      
      <div className="card">
        <div className="stats-label">Average (Last 10)</div>
        <div className="stats-value">{avgValue}</div>
      </div>
    </div>
  );
};

export default StatsCard;