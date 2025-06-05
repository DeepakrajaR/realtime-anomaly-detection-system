import React, { useState } from 'react';
import { SimulationSettings, AppSettings } from '../../types';

interface ControlPanelProps {
  onStartStream: (settings: SimulationSettings) => void;
  onStopStream: () => void;
  isStreaming: boolean;
  isConnected: boolean;
  appSettings: AppSettings;
  onChangeSettings: (settings: AppSettings) => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  onStartStream,
  onStopStream,
  isStreaming,
  isConnected,
  appSettings,
  onChangeSettings,
}) => {
  const [settings, setSettings] = useState<SimulationSettings>({
    numPoints: 1000,
    includeAnomalies: true,
    interval: 100,
  });

  const handleStartStream = () => {
    onStartStream(settings);
  };

  const handleStopStream = () => {
    onStopStream();
  };

  const handleSettingsChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    setSettings((prev) => ({
      ...prev,
      [name]: type === 'checkbox' 
        ? (e.target as HTMLInputElement).checked 
        : type === 'number' 
          ? parseInt(value, 10) 
          : value,
    }));
  };

  const handleAppSettingsChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    onChangeSettings({
      ...appSettings,
      [name]: type === 'number' ? parseInt(value, 10) : value,
    });
  };

  return (
    <div className="card mb-6">
      <h2 className="card-title">Control Panel</h2>
      
      <div className="grid grid-2">
        <div>
          <h3 className="mb-2">Data Stream Settings</h3>
          <div className="space-y-3">
            <div className="form-group">
              <label htmlFor="numPoints" className="form-label">
                Number of Points
              </label>
              <input
                type="number"
                id="numPoints"
                name="numPoints"
                className="form-input"
                value={settings.numPoints}
                onChange={handleSettingsChange}
                min={10}
                max={10000}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="interval" className="form-label">
                Interval (ms)
              </label>
              <input
                type="number"
                id="interval"
                name="interval"
                className="form-input"
                value={settings.interval}
                onChange={handleSettingsChange}
                min={10}
                max={5000}
                step={10}
              />
            </div>
            
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="includeAnomalies"
                name="includeAnomalies"
                className="checkbox"
                checked={settings.includeAnomalies}
                onChange={handleSettingsChange}
              />
              <label htmlFor="includeAnomalies" className="form-label mb-0">
                Include Anomalies
              </label>
            </div>
          </div>
        </div>
        
        <div>
          <h3 className="mb-2">Detection Settings</h3>
          <div className="space-y-3">
            <div className="form-group">
              <label htmlFor="modelType" className="form-label">
                Model Type
              </label>
              <select
                id="modelType"
                name="modelType"
                className="form-select"
                value={appSettings.modelType}
                onChange={handleAppSettingsChange}
              >
                <option value="isolation_forest">Isolation Forest</option>
                <option value="lstm">LSTM</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="windowSize" className="form-label">
                Window Size
              </label>
              <input
                type="number"
                id="windowSize"
                name="windowSize"
                className="form-input"
                value={appSettings.windowSize}
                onChange={handleAppSettingsChange}
                min={10}
                max={1000}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="threshold" className="form-label">
                Threshold
              </label>
              <input
                type="number"
                id="threshold"
                name="threshold"
                className="form-input"
                value={appSettings.threshold}
                onChange={handleAppSettingsChange}
                min={0.01}
                max={1}
                step={0.01}
              />
            </div>
          </div>
        </div>
      </div>
      
      <div className="btn-group">
        <button
          type="button"
          className={`btn ${isConnected && !isStreaming ? 'btn-primary' : 'btn-disabled'}`}
          onClick={handleStartStream}
          disabled={!isConnected || isStreaming}
        >
          Start Stream
        </button>
        
        <button
          type="button"
          className={`btn ${isStreaming ? 'btn-danger' : 'btn-disabled'}`}
          onClick={handleStopStream}
          disabled={!isStreaming}
        >
          Stop Stream
        </button>
      </div>
    </div>
  );
};

export default ControlPanel;