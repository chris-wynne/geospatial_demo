import pytest
import sys
from ....utils.utils.db_operations.connection_db import create_engine_and_conn_string, validate_database_connection
from sqlalchemy.engine.base import Engine
from unittest.mock import Mock, patch, MagicMock

def test_create_engine_and_conn_string_success():
    server = "valid_server"
    database = "valid_database"
    username = "valid_username"
    password = "valid_password"
    
    engine, conn_str = create_engine_and_conn_string(server, database, username, password)
    
    assert isinstance(engine, Engine)
    assert isinstance(conn_str, str)

@patch('sqlalchemy.create_engine')
def test_create_engine_and_conn_string_failure(mocked_engine):
    mocked_engine.side_effect = Exception("Connection error")
    server = "invalid_server"
    database = "invalid_database"
    username = "invalid_username"
    password = "invalid_password"
    
    result = create_engine_and_conn_string(server, database, username, password)
    
    assert result is None