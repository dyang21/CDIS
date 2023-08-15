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
    """
    Create a new table named 'sensor_data' in an SQLite database if it doesn't exist already.
    
    Args:
        None
        
    Returns:
        conn (sqlite3.Connection): A connection object to the SQLite database.
        c (sqlite3.Cursor): A cursor object to execute SQL commands on the database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                (temperature real, humidity real, timestamp real)''')
>>>>>>> 42f0e71 (clean up code)
    conn.commit()
    return conn, c

def consume_data(consumer: KafkaConsumer, c: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    """
    Consume data from a Kafka consumer and store it in a SQLite database.

    This function iterates through messages received by the Kafka consumer, extracts data from each message,
    inserts the data into a SQLite database table named 'sensor_data', and commits the transaction.

    Args:
        consumer (KafkaConsumer): The KafkaConsumer object.
        c (sqlite3.Cursor): The SQLite cursor for executing database queries.
        conn (sqlite3.Connection): The SQLite database connection.

    Returns:
        None
    """
    for message in consumer:
        data = message.value
        print(f"Consumed: {data}")
        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?)",
                  (data["temperature"], data["humidity"], data["timestamp"]))
        conn.commit()

def main():
    """
    Main function to initialize and handle Kafka consumer.

    This function does the following:
    1. Initializes a Kafka consumer connection to the specified bootstrap server.
    2. Calls the 'create_table' function to set up the SQLite database and obtain a cursor.
    3. Invokes the 'consume_data' function to start processing Kafka messages and storing them in the database.
    4. Handles specific exceptions like KafkaError and sqlite3.Error, as well as general exceptions.
    5. Closes the database connection after processing is complete.

    Args:
        None

    Returns:
        None

    Raises:
        KafkaError: If there is an issue connecting to the Kafka server.
        sqlite3.Error: If there is an error in SQLite database operations.
        Exception: For any other unexpected errors.
    """    
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
