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
    """
    Produces sensor data and sends it to a producer.

    This function generates sensor data using the `generate_sensor_data` function and
    sends it to the given producer on the 'sensor-data' topic. The produced data
    is also printed to the standard output.

    Parameters:
        producer (KafkaProducer): The KafkaProducer object for sending data.
    Returns:
        data (dict): The generated sensor data.
    """
    sensor_data, temperature_data, humidity_data, sensor_logs_data = generate_sensor()

    producer.send('sensor-data', value=sensor_data)
    producer.send('temperature-data', value=temperature_data)
    producer.send('humidity-data', value=humidity_data)
    producer.send('sensor_logs_data', value=sensor_logs_data)

    print(f"Produced: {sensor_data}, {temperature_data}, {humidity_data}, {sensor_logs_data}")

    return sensor_data, temperature_data, humidity_data, sensor_logs_data #Returns for testing purposes.

def main():
    """
    Main function to initialize and handle Kafka producer.

    This function does the following:
    1. Initializes a Kafka producer connection to the specified bootstrap server.
    2. Continuously calls the produce_data function to send data to Kafka.
    3. Handles specific exceptions like KafkaError and JSONDecodeError, as well as general exceptions.
    4. Sleeps for one second after each iteration of producing data.

    Args:
        None

    Returns:
        None

    Raises:
        KafkaError: An error in connecting to the Kafka server.
        json.JSONDecodeError: An error in JSON serialization while producing data.
        Exception: Any unexpected error that might occur.

    """
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
