import React from 'react';
import { AnomalyDetection } from '../../types';
import moment from 'moment';

interface AnomalyListProps {
  anomalies: AnomalyDetection[];
}

const AnomalyList: React.FC<AnomalyListProps> = ({ anomalies }) => {
  if (anomalies.length === 0) {
    return (
      <div className="card">
        <h2 className="card-title">Recent Anomalies</h2>
        <p className="status-text">No anomalies detected yet.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="card-title">Recent Anomalies</h2>
      <div style={{ overflowX: 'auto' }}>
        <table className="table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Value</th>
              <th>Score</th>
              <th>Threshold</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.slice(0, 10).map((anomaly, index) => (
              <tr key={index}>
                <td>{moment(anomaly.timestamp).format('HH:mm:ss')}</td>
                <td>{anomaly.value.toFixed(3)}</td>
                <td>
                  <span className={`badge ${
                    anomaly.score > anomaly.threshold * 1.5
                      ? 'badge-red'
                      : 'badge-orange'
                  }`}>
                    {anomaly.score.toFixed(3)}
                  </span>
                </td>
                <td>{anomaly.threshold.toFixed(3)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AnomalyList;