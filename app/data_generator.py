from kafka import KafkaProducer
from kafka.errors import KafkaError
from json import JSONDecodeError
import time
import json
import random

def generate_sensor_data():
    """
    Generates a dictionary containing sensor data.

    This function simulates the collection of data from a sensor, 
    including temperature, humidity, and a timestamp.

    Returns:
        data (dict): It contains the following keys:
            - "temperature": A random float ranging from 20 to 25.
            - "humidity": A random float ranging from 30 to 40.
            - "timestamp": A float representing the current time.
    """
    data = {
        "temperature": random.uniform(20, 25),
        "humidity": random.uniform(30, 40),
        "timestamp": time.time()
    }
    return data

def produce_data(producer):
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
    data = generate_sensor_data()
    producer.send('sensor-data', value=data)
    print(f"Produced: {data}")
    return data #Returns for testing purposes.
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
