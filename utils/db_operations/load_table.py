import pandas as pd
import logging
import sys

import sqlalchemy
from sqlalchemy import text

from ..logger.default_logger import PrintLogger

def load_data_df(data, engine, table_name, schema, if_exists="replace", logger=PrintLogger()):
    """
    Load data into a database table using SQLAlchemy and Pandas.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be loaded.
        engine (sqlalchemy.engine.base.Connection): The SQLAlchemy database engine connection.
        table_name (str): The name of the database table to which the data will be loaded.
        schema (str): The schema name of the database table.
        logger (Logger, optional): The logger object for logging transaction and error messages.
                                   Default is PrintLogger().

    Returns:
        None
    """
    with engine.connect() as conn:  # Ensure proper connection management
        transaction = conn.begin()  # Start a new transaction
        logger.info("Transaction initiated.")
        try:
            data.to_sql(table_name, schema=schema, con=conn, index=False, if_exists=if_exists)
            transaction.commit()  # commit transaction
            logger.info("Data committed successfully.")
        except Exception as e:
            transaction.rollback()
            logger.error(f"An error occurred, rolled back transaction. Error: {e}") # Records load error
            sys.exit(1)  # Exiting the script with a non-zero value to indicate an error
            raise
    logger.info("Transaction ended.")
    
    return None