from kafka import KafkaConsumer
from kafka.errors import KafkaError
import sqlite3
import json

<<<<<<< HEAD

conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (temperature real, humidity real, timestamp real)''')


consumer = KafkaConsumer(
    'sensor-data',
     bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
     value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    data = message.value
    print(f"Consumed: {data}")


    c.execute("INSERT INTO sensor_data VALUES (?, ?, ?)",
              (data["temperature"], data["humidity"], data["timestamp"]))


=======
db_path = os.path.join(os.sep, 'my-pv', 'sensor_data.db')

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                (temperature real, humidity real, timestamp real)''')
>>>>>>> 42f0e71 (clean up code)
    conn.commit()
    return conn, c

def consume_data(consumer, c, conn):
    for message in consumer:
        data = message.value
        print(f"Consumed: {data}")
        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?)",
                  (data["temperature"], data["humidity"], data["timestamp"]))
        print("About to commit...")
        conn.commit()

def main():
    try:
        consumer = KafkaConsumer(
            'sensor-data',
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
