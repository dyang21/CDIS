from kafka import KafkaConsumer
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
    return conn

def main():
    conn = create_table()
    c = conn.cursor()

    consumer = KafkaConsumer(
        'sensor-data',
         bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    for message in consumer:
        data = message.value
        print(f"Consumed: {data}")

        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?)",
                  (data["temperature"], data["humidity"], data["timestamp"]))

        conn.commit()

    conn.close()

if __name__ == "__main__":
    main()