from unittest.mock import MagicMock, patch
import sqlite3
import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import data_processor

def test_consume_data():
    """
    Test the consume_data function from the data_processor module.

    This test checks the following:
    1. The SQLite connection's execute method is called with the correct arguments.
    2. The commit method of the SQLite connection is called once after insertion.

    Mocks:
        - Kafka Consumer: To emulate the behavior of receiving a message from a Kafka topic.
        - SQLite Connection and Cursor: To prevent actual database interactions and to 
          validate the SQL execution and commit operations.
    """
    sensor_msg_mock = MagicMock()
    sensor_msg_mock.value = json.dumps({"sensor_id": 1, "location": "Room 1", "sensor_type": "Temperature"})
    sensor_msg_mock.topic = 'sensor-table'

    temp_msg_mock = MagicMock()
    temp_msg_mock.value = json.dumps({"sensor_id": 1, "temperature": 24.5, "timestamp": 10000000.0})
    temp_msg_mock.topic = 'temperature-data-table'

    humidity_msg_mock = MagicMock()
    humidity_msg_mock.value = json.dumps({"sensor_id": 1, "humidity": 35.0, "timestamp": 10000000.0})
    humidity_msg_mock.topic = 'humidity-data-table'

    log_msg_mock = MagicMock()
    log_msg_mock.value = json.dumps({"sensor_id": 1, "logs_date": 10000000.0, "details": "Maintenance"})
    log_msg_mock.topic = 'sensor-logs-table'

    consumer_mock = MagicMock()
    consumer_mock.__iter__.side_effect = lambda: iter([sensor_msg_mock, temp_msg_mock, humidity_msg_mock, log_msg_mock])

    mock_conn_instance = MagicMock(spec=sqlite3.Connection)
    mock_c = MagicMock()
    mock_conn_instance.cursor.return_value = mock_c

    with patch('sqlite3.connect', return_value=mock_conn_instance):
        data_processor.consume_data(consumer_mock, mock_c, mock_conn_instance)

        assert mock_c.execute.call_count == 4
        mock_c.execute.assert_any_call(
            "INSERT INTO sensor (sensor_id, location, sensor_type) VALUES (?, ?, ?)",
            (1, "Room 1", "Temperature")
        )
        mock_c.execute.assert_any_call(
            "INSERT INTO temperature_data (temperature, timestamp, sensor_id) VALUES (?, ?, ?)",
            (24.5, 10000000.0, 1)
        )
        mock_c.execute.assert_any_call(
            "INSERT INTO humidity_data (humidity, timestamp, sensor_id) VALUES (?, ?, ?)",
            (35.0, 10000000.0, 1)
        )
        mock_c.execute.assert_any_call(
            "INSERT INTO sensor_logs (logs_date, details, sensor_id) VALUES (?, ?, ?)",
            (10000000.0, "Maintenance", 1)
        )

        mock_conn_instance.commit.assert_called_once()