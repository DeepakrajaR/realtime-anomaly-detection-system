import React, { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <header className="header">
        <div className="container">
          <h1>Real-time Anomaly Detection System</h1>
          <p>Detect and visualize anomalies in streaming data</p>
        </div>
      </header>
      
      <main className="main container">
        {children}
      </main>
      
      <footer className="footer">
        <div className="container">
          <p>
            Real-time Anomaly Detection System &copy; {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;