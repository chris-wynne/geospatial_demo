import sys
import logging
import sqlalchemy
from urllib.parse import quote_plus

from ..logger.default_logger import PrintLogger

def create_engine_and_conn_string_mssql(server, database, username, password, logger=PrintLogger()):
    """
    Creates a SQLAlchemy engine and generates a connection string for an Azure MSSQL database with the provided credentials.

    Args:
        server (str): The address of the SQL server (e.g., 'your_server.database.windows.net').
        database (str): The name of the database to connect to.
        username (str): The username for the database login.
        password (str): The password for the database login.
        logger (object): A logging object with info, error, and debug methods. Defaults to an instance of PrintLogger.

    Returns:
        sqlalchemy.engine.base.Engine or None: A SQLAlchemy engine object if the connection is successful, or None if the connection fails.

    Note:
        Ensure that the ODBC Driver 17 for SQL Server is installed on your system. Credentials should be managed securely.
    """
    password = quote_plus(password)
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    try:
        logger.info("Creating SQLAlchemy engine & connection string...")
        engine = sqlalchemy.create_engine(connection_string, echo=False)
        logger.info("Engine & connection string created successfully using SQLAlchemy!")
        return engine, connection_string
    except Exception as e:
        logger.error("Error creating engine using SQLAlchemy: %s", e)
        return None
    
    
def create_engine_and_conn_string_postgres(server, database, username, password, port=5432, logger=PrintLogger()):
    """
    Creates a SQLAlchemy engine and generates a connection string for a local PostgreSQL database with the provided credentials.

    Args:
        server (str): The address of the PostgreSQL server, typically 'localhost' for a local database.
        database (str): The name of the database to connect to.
        username (str): The username for the database login.
        password (str): The password for the database login.
        port (int): The port on which the PostgreSQL server is running, defaults to 5432.
        logger (object): A logging object with info, error, and debug methods. Defaults to an instance of PrintLogger.

    Returns:
        sqlalchemy.engine.base.Engine or None: A SQLAlchemy engine object if the connection is successful, or None if the connection fails.

    Note:
        Ensure that psycopg2 is installed on your system. Credentials should be managed securely.
    """
    password = quote_plus(password)
    connection_string = f"postgresql+psycopg2://{username}:{password}@{server}:{port}/{database}"
    try:
        logger.info("Creating SQLAlchemy engine & connection string for PostgreSQL...")
        engine = sqlalchemy.create_engine(connection_string, echo=False)
        logger.info("Engine & connection string created successfully using SQLAlchemy for PostgreSQL!")
        return engine, connection_string
    except Exception as e:
        logger.error("Error creating engine using SQLAlchemy for PostgreSQL: %s", e)
        return None
    
def validate_database_connection(engine, logger=PrintLogger()):
    """
    Validates the database connection using the provided SQLAlchemy engine.

    If the connection test is successful, it logs a success message.
    If the connection test fails, or if the engine is not provided, it logs an error and exits the script.

    Args:
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine object to test the connection.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    if engine:
        try:
            logger.info("Validating database connection...")
            with engine.connect() as connection:
                logger.info("Database connection validated")
                return True
                # Connection is automatically closed here, when the 'with' block is exited
        except Exception as e:
            logger.error(f"Test connection failed: {e}")
            return False
    else:
        logger.error("Engine object is None, cannot test connection")
        return False
