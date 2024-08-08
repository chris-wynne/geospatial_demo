import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

from ..logger.default_logger import PrintLogger

def check_table_exists(engine, schema_name, table_name, logger=PrintLogger()):
    """
    Checks if a specified table exists in a given schema within a SQL database using SQLAlchemy.

    Args:
        engine: SQLAlchemy engine object.
        schema_name (str): The name of the schema in which to check for the table.
        table_name (str): The name of the table to check for existence.
        logger (Logger, optional): Logger object for logging messages. Defaults to PrintLogger().

    Returns:
        bool: True if the table exists, False otherwise.
    """
    try:
        # Create a MetaData instance
        metadata = MetaData()

        # Reflect metadata
        with engine.connect() as conn:
            metadata.reflect(bind=conn, schema=schema_name, only=[table_name])

        # Check if table exists
        full_table_name = f"{schema_name}.{table_name}" if schema_name else table_name
        exists = full_table_name in metadata.tables

        # Log the result
        logger.info(f"Table '{table_name}' existence in schema '{schema_name}': {exists}")
        return exists

    except SQLAlchemyError as e:
        logger.info(f"Table '{table_name}' existence in schema '{schema_name}': False")
        return False