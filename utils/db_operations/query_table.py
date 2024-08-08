import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from ..logger.default_logger import PrintLogger

def query_database_to_df(engine, sql_query, logger=PrintLogger() ,params=None):
    """
    Executes a query from a .sql file using an SQLAlchemy engine and returns a pandas DataFrame.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.
        sql_query (str): sql query string.
        params (dict, optional): A dictionary of parameters for the query, to be used with named parameters in the SQL. Defaults to None.

    Returns:
        dataframe: A pandas DataFrame containing the retrieved rows.
    """  
    logger.info(f"Executing SQL query")

    # Use the engine in a context manager to ensure proper resource management
    with engine.connect() as conn:
        # Execute the query with optional parameters
        if params is not None:
            query_result = conn.execute(text(sql_query), **params)
        else:
            query_result = conn.execute(text(sql_query))
        
        df = pd.DataFrame(query_result.fetchall(), columns=query_result.keys())

    logger.info("Query executed and results retrieved successfully.")
    return df


def query_database_to_gdf(engine, sql_query, logger=PrintLogger(), params=None, geom_col='geometry'):
    """
    Executes a query from a .sql file using an SQLAlchemy engine and returns a GeoPandas GeoDataFrame.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.
        sql_query (str): sql query string.
        params (dict, optional): A dictionary of parameters for the query, to be used with named parameters in the SQL. Defaults to None.
        geom_col (str): The name of the column containing the geometry data. Defaults to 'geometry'.

    Returns:
        geodataframe: A GeoPandas GeoDataFrame containing the retrieved rows and geometry.
    """
   
    logger.info(f"Executing SQL query")

    # Use the engine in a context manager to ensure proper resource management
    with engine.connect() as conn:
        # Execute the query with optional parameters
        if params is not None:
            query_result = conn.execute(text(sql_query), **params)
        else:
            query_result = conn.execute(text(sql_query))
        
        # Create a DataFrame from the query result
        df = pd.DataFrame(query_result.fetchall(), columns=query_result.keys())

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geom_col)

    logger.info("Query executed and GeoDataFrame created successfully.")
    return gdf


def run_sql_script(engine, script_path, logger=PrintLogger()):
    """
    Executes SQL commands from a script file using an SQLAlchemy engine.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.
        script_path (str): The file path of the SQL script.
        logger (PrintLogger, optional): Logger for logging messages. Defaults to PrintLogger().
    """
    # Read the SQL script
    with open(script_path, 'r') as file:
        sql_script = file.read()

    logger.info(f"Executing SQL script from {script_path}")

    # Execute the SQL script
    with engine.connect() as connection:
        try:
            connection.execute(sql_script)
            logger.info("SQL script executed successfully.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            
            
def check_table_has_data(engine, schema, table_name, logger):
    """
    Check if a specified table in a given schema contains any data.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.
        schema (str): The schema name of the table.
        table_name (str): The name of the table to check.
        logger (object): A logger object for logging messages.

    Returns:
        bool: True if the table has data, False otherwise.
    """

    logger.info(f'Executing query to check if "{schema}"."{table_name}" has data.')

    query = text(f'SELECT EXISTS (SELECT 1 FROM "{schema}"."{table_name}" LIMIT 1);')

    try:
        with engine.connect() as connection:
            result = connection.execute(query).scalar()
            if result:
                logger.info("Table contains data.")
                return True
            else:
                logger.info("Table is empty.")
                return False
    except SQLAlchemyError as e:
        logger.error(f"An error occurred: {e}")
        return False