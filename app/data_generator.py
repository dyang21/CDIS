from kafka import KafkaProducer
from kafka.errors import KafkaError
from json import JSONDecodeError
from typing import Dict
import time
import json
import random

locations = []

def generate_sensor() -> tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:

    sensor_id = random.randint(1, 100)
    location = random.choice(["AZ", "NY", "OH", "PA", "MT", "NH", "VA"]),
    sensor_type = random.choice(['Temperature','Humidity'])

    sensor_data = {
        "sensor_id": sensor_id,
        "location": location,
        "sensor_type": sensor_type
    }
    temperature_data = {
        "sensor_id": sensor_id,
        "temperature": random.uniform(20, 80),
        "timestamp": time.time()
    }

    humidity_data = {
        "sensor_id": sensor_id,
        "humidity": random.uniform(20,80),
        "timestamp": time.time()
    }

    sensor_logs_data = {
        "sensor_id": sensor_id,
        "logs_date": time.time(),
        "details": random.choice(['Maintenance', 'Replacement', 'Inspection'])
    }



    return sensor_data, temperature_data, humidity_data, sensor_logs_data





def produce_data(producer) -> tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    sensor_data, temperature_data, humidity_data, sensor_logs_data = generate_sensor()

    producer.send('sensor-data', value=sensor_data)
    producer.send('temperature-data', value=temperature_data)
    producer.send('humidity-data', value=humidity_data)
    producer.send('sensor_logs_data', value=sensor_logs_data)

    print(f"Produced: {sensor_data}, {temperature_data}, {humidity_data}, {sensor_logs_data}")

    return sensor_data, temperature_data, humidity_data, sensor_logs_data #Returns for testing purposes.

def main():
    try:
        producer = KafkaProducer(
            bootstrap_servers='my-kafka.default.svc.cluster.local:9092', #Looks for a service named my-kafka in default namespace in port 9092.
            value_serializer=lambda v: json.dumps(v).encode('utf-8')) # This lambda function takes a Python object as input, converts it to its JSON string representation, then encodes that string as bytes.
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
            return
        except Exception as e:
            print(f"Unexpected error while producing data: {str(e)}")
            return
        time.sleep(1)


if __name__ == "__main__":
    main()
