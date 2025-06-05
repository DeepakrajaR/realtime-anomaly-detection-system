import React from 'react';

interface StatusIndicatorProps {
  isConnected: boolean;
  isStreaming: boolean;
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ isConnected, isStreaming }) => {
  return (
    <div className="status-container">
      <div className="status-item">
        <div className={`status-indicator ${isConnected ? 'status-green' : 'status-red'}`}></div>
        <span className="status-text">
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
      
      <div className="status-item">
        <div className={`status-indicator ${isStreaming ? 'status-blue' : 'status-gray'}`}></div>
        <span className="status-text">
          {isStreaming ? 'Streaming' : 'Idle'}
        </span>
      </div>
    </div>
  );
};

export default StatusIndicator;