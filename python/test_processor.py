from unittest.mock import MagicMock, patch
import sqlite3
import data_processor  

def test_consume_data():
    consumer_mock = MagicMock()
    message_mock = MagicMock()
    message_mock.value = {"temperature": 24.5, "humidity": 35.0, "timestamp": 10000000.0}
    consumer_mock.__iter__.side_effect = lambda: iter([message_mock]) 

    mock_conn_instance = MagicMock(spec=sqlite3.Connection)  
    mock_c = MagicMock()  
    mock_conn_instance.cursor.return_value = mock_c  

    with patch('sqlite3.connect', return_value=mock_conn_instance) as mock_conn:
        data_processor.consume_data(consumer_mock, mock_c, mock_conn_instance)

        mock_c.execute.assert_called_once_with(
            "INSERT INTO sensor_data VALUES (?, ?, ?)",
            (24.5, 35.0, 10000000.0)
        )
        mock_conn_instance.commit.assert_called_once()  
