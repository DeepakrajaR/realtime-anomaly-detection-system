import { useEffect, useState } from 'react';
import { socketService } from '../services/socket';
import { SocketHandlers, DataPoint, AnomalyDetection, SimulationSettings } from '../types';

export function useSocket(apiUrl: string, handlers: SocketHandlers) {
  const [isConnected, setIsConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    // Set up socket connection
    socketService.init(apiUrl);
    
    // Set socket handlers with connection state
    socketService.setHandlers({
      ...handlers,
      onConnect: () => {
        setIsConnected(true);
        handlers.onConnect?.();
      },
      onDisconnect: () => {
        setIsConnected(false);
        setIsStreaming(false);
        handlers.onDisconnect?.();
      }
    });

    // Clean up on unmount
    return () => {
      socketService.disconnect();
    };
  }, [apiUrl, handlers]);

  // Start data stream
  const startStream = (settings: SimulationSettings) => {
    socketService.startStream(settings);
    setIsStreaming(true);
  };

  // Stop data stream
  const stopStream = () => {
    socketService.stopStream();
    setIsStreaming(false);
  };

  return { 
    isConnected, 
    isStreaming, 
    startStream, 
    stopStream 
  };
}