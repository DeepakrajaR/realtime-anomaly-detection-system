// Data point from the API
export interface DataPoint {
  timestamp: string;
  value: number;
  is_anomaly: boolean;
}

// Anomaly detection from the API
export interface AnomalyDetection {
  timestamp: string;
  value: number;
  score: number;
  threshold: number;
  index: number;
}

// Socket event handlers
export interface SocketHandlers {
  onConnect?: () => void;
  onDisconnect?: () => void;
  onDataPoint?: (data: DataPoint) => void;
  onAnomalyDetected?: (data: AnomalyDetection) => void;
}

// Chart data for visualization
export interface ChartData extends DataPoint {
  id: number;
}

// Settings for data simulation
export interface SimulationSettings {
  numPoints: number;
  includeAnomalies: boolean;
  interval: number;
}

// Application settings
export interface AppSettings {
  modelType: 'isolation_forest' | 'lstm';
  windowSize: number;
  threshold: number;
}