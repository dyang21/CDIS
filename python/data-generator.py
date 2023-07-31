from kafka import KafkaProducer
import time
import json
import random

def generate_sensor_data():
    data = {
        "temperature": random.uniform(20, 25),
        "humidity": random.uniform(30, 40),
        "timestamp": time.time()
    }
    return data  # return as Python dict

producer = KafkaProducer(
    bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))


while True:
    data = generate_sensor_data()
    producer.send('sensor-data', value=data)
    print(f"Produced: {data}")
    time.sleep(1)  # generate new data every second
