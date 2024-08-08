from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

from ...logger.default_logger import PrintLogger

def set_table_stsrid(epsg_number, engine, table_name, schema, geom_col="geometry", logger=PrintLogger()):
    """
    Update the SRID (Spatial Reference System Identifier) of a specified geometry column in a database table.

    Args:
        epsg_number (int): The EPSG code representing the spatial reference system.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object connected to the database.
        table_name (str): Name of the table in the database to be updated.
        schema (str): Name of the schema in which the table exists.
        geom_col (str, optional): The name of the geometry column to update. Defaults to "geometry".
        logger (object, optional): An instance of a logger to record information and errors. Defaults to PrintLogger().

    Raises:
        Exception: If any error occurs during the SQL execution, it is logged and re-raised.
    """
    
    sql = text(f"""
    UPDATE [{schema}].[{table_name}]
    SET {geom_col}.STSrid = {epsg_number};
    """)
       
    try:
        logger.info(f"Updating SRID for: {table_name}")
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(sql)
            logger.info(f"SRID updated")
    except Exception as e:
        logger.error(f"Failed to update SRID: {e}", exc_info=True)
        
def add_stsrid_constraint(epsg_number, engine, table_name, schema, geom_col="geometry", logger=None):
    # Constructing the SQL command with proper formatting
    sql = text(f"""
    ALTER TABLE [{schema}].[{table_name}]
    ADD CONSTRAINT {geom_col}_{epsg_number}_SRID
    CHECK ({geom_col}.STSrid = {epsg_number});
    """)

    try:
        logger.info(f"Adding SRID constraint to: {table_name}.{geom_col}") if logger else print(f"Adding SRID constraint to: {table_name}.{geom_col}")
        with engine.connect() as conn:
            conn.execute(sql)
        logger.info(f"SRID constraint added successfully") if logger else print(f"SRID constraint added successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to add SRID constraint: {e}", exc_info=True) if logger else print(f"Failed to add SRID constraint: {e}")
