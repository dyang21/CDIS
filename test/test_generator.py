from kafka import KafkaProducer
from unittest.mock import Mock, patch
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import data_generator
def test_produce_data():
    """
    Test the produce_data function from the data_generator module.

    This test checks the following:
    - The KafkaProducer's send method is called once.

    Mocks:
        KafkaProducer: To prevent actual Kafka interactions and to validate 
                       that the `send` method is called.
                    
    """
    with patch('app.data_generator.KafkaProducer', return_value=Mock(spec=KafkaProducer)) as mock_producer: #Replace the real KafkaProducer with a mock object.
        sensor_data, temperature_data, humidity_data, sensor_logs_data = data_generator.produce_data(mock_producer)
        mock_producer.send.assert_called_once()
        assert 'sensor_id' in sensor_data
        assert 'location' in sensor_data
        assert 'sensor_type' in sensor_data

        assert 'sensor_id' in temperature_data
        assert 'temperature' in temperature_data
        assert 'timestamp' in temperature_data

        assert 'sensor_id' in humidity_data
        assert 'humidity' in humidity_data
        assert 'timestamp' in humidity_data

        assert 'sensor_id' in sensor_logs_data
        assert 'logs_date' in sensor_logs_data
        assert 'details' in sensor_logs_data