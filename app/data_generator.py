from kafka import KafkaProducer
from kafka.errors import KafkaError
from json import JSONDecodeError
import time
import json
import random

def generate_sensor_data():
    data = {
        "temperature": random.uniform(20, 25),
        "humidity": random.uniform(30, 40),
        "timestamp": time.time()
    }
    return data

def produce_data(producer):
    data = generate_sensor_data()
    producer.send('sensor-data', value=data)
    print(f"Produced: {data}")
    return data

def main():
    try:
        producer = KafkaProducer(
            bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    except KafkaError as e:
        print(f"Kafka connection error: {str(e)}")
        return
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return

    while True:
        try:
            produce_data(producer)
        except json.JSONDecodeError as e:
            print(f"JSON serialization error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error while producing data: {str(e)}")
        time.sleep(1)


if __name__ == "__main__":
    main()
