import React, { useState, useEffect } from 'react';
import Layout from './components/layout/Layout';
import StatusIndicator from './components/layout/StatusIndicator';
import ControlPanel from './components/dashboard/ControlPanel';
import RealtimeChart from './components/charts/RealtimeChart';
import AnomalyList from './components/dashboard/AnomalyList';
import StatsCard from './components/dashboard/StatsCard';
import AnomalyAlert from './components/alerts/AnomalyAlert';
import { useSocket } from './hooks/useSocket';
import { ChartData, DataPoint, AnomalyDetection, AppSettings } from './types';

const App: React.FC = () => {
  // API URL from environment or default
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
  
  // State for data and settings
  const [dataPoints, setDataPoints] = useState<ChartData[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyDetection[]>([]);
  const [appSettings, setAppSettings] = useState<AppSettings>({
    modelType: 'isolation_forest',
    windowSize: 100,
    threshold: 0.05,
  });

  // Socket connection with handlers
  const { isConnected, isStreaming, startStream, stopStream } = useSocket(
    apiUrl,
    {
      onDataPoint: (data: DataPoint) => {
        setDataPoints((prev) => {
          // Create new data point with ID
          const newPoint: ChartData = {
            ...data,
            id: prev.length > 0 ? prev[prev.length - 1].id + 1 : 0,
          };
          
          // Keep only the last 100 points
          const newData = [...prev, newPoint].slice(-100);
          return newData;
        });
      },
      onAnomalyDetected: (data: AnomalyDetection) => {
        setAnomalies((prev) => [...prev, data].slice(-20));
      },
    }
  );

  // Reset data when streaming stops
  useEffect(() => {
    if (!isStreaming) {
      // Keep data on screen but don't accumulate more
    }
  }, [isStreaming]);

  return (
    <Layout>
      <div className="flex justify-between items-center mb-6">
        <h2 className="card-title">Dashboard</h2>
        <StatusIndicator isConnected={isConnected} isStreaming={isStreaming} />
      </div>
      
      <ControlPanel
        onStartStream={startStream}
        onStopStream={stopStream}
        isStreaming={isStreaming}
        isConnected={isConnected}
        appSettings={appSettings}
        onChangeSettings={setAppSettings}
      />
      
      <StatsCard data={dataPoints} anomalies={anomalies} />
      
      <div className="card mb-6">
        <h2 className="card-title">Real-time Data Stream</h2>
        <RealtimeChart data={dataPoints} height={300} />
      </div>
      
      <AnomalyList anomalies={anomalies} />
      
      <AnomalyAlert anomalies={anomalies} />
    </Layout>
  );
};

export default App;