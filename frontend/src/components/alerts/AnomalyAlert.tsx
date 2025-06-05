import React, { useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AnomalyDetection } from '../../types';

interface AnomalyAlertProps {
  anomalies: AnomalyDetection[];
}

const AnomalyAlert: React.FC<AnomalyAlertProps> = ({ anomalies }) => {
  useEffect(() => {
    // Show toast notification when a new anomaly is detected
    if (anomalies.length > 0) {
      const latestAnomaly = anomalies[anomalies.length - 1];
      
      toast.error(
        <div>
          <h4 className="font-bold">Anomaly Detected!</h4>
          <p>Value: {latestAnomaly.value.toFixed(3)}</p>
          <p>Score: {latestAnomaly.score.toFixed(3)}</p>
          <p>Time: {new Date(latestAnomaly.timestamp).toLocaleTimeString()}</p>
        </div>,
        {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        }
      );
    }
  }, [anomalies]);

  return (
    <ToastContainer
      position="top-right"
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
    />
  );
};

export default AnomalyAlert;