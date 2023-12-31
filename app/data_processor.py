from kafka import KafkaConsumer
from kafka.errors import KafkaError
import sqlite3
import json
import os

db_path = os.path.join(os.sep, 'my-pv', 'sensor_data.db')

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS sensor (
                    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT,
                    sensor_type TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS temperature_data (
                    temp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER,
                    temperature REAL,
                    timestamp REAL,
                    FOREIGN KEY(sensor_id) REFERENCES sensor(sensor_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS humidity_data (
                    humidity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER,
                    humidity REAL,
                    timestamp REAL,
                    FOREIGN KEY(sensor_id) REFERENCES sensor(sensor_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_logs(
                    logs_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER,
                    logs_date REAL,
                    details TEXT,
                    FOREIGN KEY(sensor_id) REFERENCES sensor(sensor_id))''')
    
    conn.commit()
    return conn, c

def consume_data(consumer: KafkaConsumer, c: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for message in consumer:
        data = message.value

        if message.topic == 'sensor-table':
            c.execute("INSERT INTO sensor (sensor_id, location, sensor_type) VALUES (?, ?, ?)",
                      (data["sensor_id"], data["location"], data["sensor_type"]))

        elif message.topic == 'temperature-data-table':
            c.execute("INSERT INTO temperature_data (temperature, timestamp, sensor_id) VALUES (?, ?, ?)",
                      (data["temperature"], data["timestamp"], data["sensor_id"]))

        elif message.topic == 'humidity-data-table':
            c.execute("INSERT INTO humidity_data (humidity, timestamp, sensor_id) VALUES (?, ?, ?)",
                      (data["humidity"], data["timestamp"], data["sensor_id"]))

        elif message.topic == 'sensor-logs-table':
            c.execute("INSERT INTO sensor_logs (logs_date, details, sensor_id) VALUES (?, ?, ?)",
                      (data["logs_date"], data["details"], data["sensor_id"]))
    
        conn.commit()
    conn.close()

def main():
    try:
        consumer = KafkaConsumer(
            'sensor-table',
            'temperature-data-table',
            'humidity-data-table',
            'sensor-logs-table',
            bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    except KafkaError as e:
        print(f"Kafka connection error: {str(e)}")
        return
    try:
        conn, c = create_table()
        consume_data(consumer, c, conn)
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error while consuming data: {str(e)}")

    conn.close()

if __name__ == "__main__":
    main()
