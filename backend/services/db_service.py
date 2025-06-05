import psycopg2
import redis
import json
from datetime import datetime

class DatabaseService:
    """Service for database operations"""
    
    def __init__(self, postgres_url=None, redis_url=None):
        """Initialize the database service
        
        Args:
            postgres_url: PostgreSQL connection URL
            redis_url: Redis connection URL
        """
        self.postgres_url = postgres_url
        self.redis_url = redis_url
        self.postgres_conn = None
        self.redis_conn = None
        
    def connect_postgres(self):
        """Connect to PostgreSQL database"""
        if self.postgres_url and not self.postgres_conn:
            self.postgres_conn = psycopg2.connect(self.postgres_url)
            
            # Create tables if they don't exist
            self._create_tables()
            
    def connect_redis(self):
        """Connect to Redis database"""
        if self.redis_url and not self.redis_conn:
            self.redis_conn = redis.from_url(self.redis_url)
            
    def _create_tables(self):
        """Create database tables if they don't exist"""
        with self.postgres_conn.cursor() as cursor:
            # Enable TimescaleDB extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
            
            # Create data points table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_points (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL,
                    value FLOAT NOT NULL,
                    is_anomaly BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Create hypertable for time-series data
            cursor.execute("""
                SELECT create_hypertable('data_points', 'timestamp', 
                                        if_not_exists => TRUE)
            """)
            
            # Create anomalies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anomalies (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL,
                    data_point_id INTEGER REFERENCES data_points(id),
                    score FLOAT NOT NULL,
                    model_type VARCHAR(50) NOT NULL
                )
            """)
            
            self.postgres_conn.commit()
            
    def store_data_point(self, timestamp, value, is_anomaly=False):
        """Store a data point in PostgreSQL
        
        Args:
            timestamp: ISO format timestamp or datetime object
            value: Numeric value of the data point
            is_anomaly: Whether this point is an anomaly
            
        Returns:
            ID of the inserted record
        """
        if not self.postgres_conn:
            self.connect_postgres()
            
        # Convert string timestamp to datetime if needed
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO data_points (timestamp, value, is_anomaly)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (timestamp, value, is_anomaly))
            
            row_id = cursor.fetchone()[0]
            self.postgres_conn.commit()
            
            return row_id
            
    def store_anomaly(self, timestamp, data_point_id, score, model_type):
        """Store an anomaly detection in PostgreSQL
        
        Args:
            timestamp: ISO format timestamp or datetime object
            data_point_id: ID of the related data point
            score: Anomaly score
            model_type: Type of detection model used
            
        Returns:
            ID of the inserted record
        """
        if not self.postgres_conn:
            self.connect_postgres()
            
        # Convert string timestamp to datetime if needed
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO anomalies (timestamp, data_point_id, score, model_type)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (timestamp, data_point_id, score, model_type))
            
            row_id = cursor.fetchone()[0]
            self.postgres_conn.commit()
            
            return row_id
            
    def cache_recent_data(self, data, key='recent_data', expire_seconds=3600):
        """Cache data in Redis
        
        Args:
            data: Data to cache (will be JSON serialized)
            key: Redis key to use
            expire_seconds: TTL in seconds
        """
        if not self.redis_conn:
            self.connect_redis()
            
        # JSON serialize data
        serialized = json.dumps(data)
        
        # Store in Redis with expiration
        self.redis_conn.setex(key, expire_seconds, serialized)
        
    def get_cached_data(self, key='recent_data'):
        """Get cached data from Redis
        
        Args:
            key: Redis key to retrieve
            
        Returns:
            Deserialized data or None if not found
        """
        if not self.redis_conn:
            self.connect_redis()
            
        # Get data from Redis
        data = self.redis_conn.get(key)
        
        # Return deserialized data if found
        if data:
            return json.loads(data)
        else:
            return None
            
    def get_recent_data_points(self, limit=100):
        """Get recent data points from PostgreSQL
        
        Args:
            limit: Maximum number of points to retrieve
            
        Returns:
            List of data points
        """
        if not self.postgres_conn:
            self.connect_postgres()
            
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, timestamp, value, is_anomaly
                FROM data_points
                ORDER BY timestamp DESC
                LIMIT %s
            """, (limit,))
            
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'timestamp': row[1].isoformat(),
                    'value': row[2],
                    'is_anomaly': row[3]
                })
                
            return result
            
    def get_recent_anomalies(self, limit=20):
        """Get recent anomalies from PostgreSQL
        
        Args:
            limit: Maximum number of anomalies to retrieve
            
        Returns:
            List of anomalies
        """
        if not self.postgres_conn:
            self.connect_postgres()
            
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.timestamp, a.score, a.model_type, 
                       d.value, d.id as data_point_id
                FROM anomalies a
                JOIN data_points d ON a.data_point_id = d.id
                ORDER BY a.timestamp DESC
                LIMIT %s
            """, (limit,))
            
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'timestamp': row[1].isoformat(),
                    'score': row[2],
                    'model_type': row[3],
                    'value': row[4],
                    'data_point_id': row[5]
                })
                
            return result
    
    def close(self):
        """Close database connections"""
        if self.postgres_conn:
            self.postgres_conn.close()
            self.postgres_conn = None
            
        if self.redis_conn:
            self.redis_conn.close()
            self.redis_conn = None