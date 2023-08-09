from kafka import KafkaProducer
from unittest.mock import Mock, patch
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import data_generator
def test_produce_data():
    with patch('app.data_generator.KafkaProducer', return_value=Mock(spec=KafkaProducer)) as mock_producer:
        data = data_generator.produce_data(mock_producer)
        mock_producer.send.assert_called_once()
        assert 'temperature' in data
        assert 'humidity' in data
        assert 'timestamp' in data
