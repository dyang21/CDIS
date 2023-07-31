from kafka import KafkaConsumer
import sqlite3
import json


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


    conn.commit()


conn.close()
