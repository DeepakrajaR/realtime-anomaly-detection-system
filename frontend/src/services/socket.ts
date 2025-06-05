import { io, Socket } from 'socket.io-client';
import { SocketHandlers, SimulationSettings } from '../types';

class SocketService {
  private socket: Socket | null = null;
  private handlers: SocketHandlers = {};

  // Initialize the socket connection
  init(url: string): void {
    if (this.socket) {
      this.socket.disconnect();
    }

    this.socket = io(url);

    // Set up event listeners
    this.socket.on('connect', () => {
      console.log('Socket connected');
      if (this.handlers.onConnect) {
        this.handlers.onConnect();
      }
    });

    this.socket.on('disconnect', () => {
      console.log('Socket disconnected');
      if (this.handlers.onDisconnect) {
        this.handlers.onDisconnect();
      }
    });

    this.socket.on('data_point', (data) => {
      if (this.handlers.onDataPoint) {
        this.handlers.onDataPoint(data);
      }
    });

    this.socket.on('anomaly_detected', (data) => {
      if (this.handlers.onAnomalyDetected) {
        this.handlers.onAnomalyDetected(data);
      }
    });
  }

  // Set event handlers
  setHandlers(handlers: SocketHandlers): void {
    this.handlers = handlers;
  }

  // Start data stream simulation
  startStream(settings: SimulationSettings): void {
    if (!this.socket) {
      console.error('Socket not initialized');
      return;
    }

    this.socket.emit('start_stream', {
      num_points: settings.numPoints,
      include_anomalies: settings.includeAnomalies,
    });
  }

  // Stop data stream simulation
  stopStream(): void {
    if (!this.socket) {
      console.error('Socket not initialized');
      return;
    }

    this.socket.emit('stop_stream');
  }

  // Disconnect the socket
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // Check if socket is connected
  isConnected(): boolean {
    return !!this.socket?.connected;
  }
}

// Export a singleton instance
export const socketService = new SocketService();