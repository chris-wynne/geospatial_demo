import logging
from sqlalchemy import create_engine, Table, Column, MetaData, Float, NVARCHAR, String, TEXT, Integer, Boolean, DateTime, Text
from sqlalchemy.types import UserDefinedType
from geoalchemy2 import Geometry

from ..logger.default_logger import PrintLogger

# Custom type for sys.geometry
class SysGeometry(UserDefinedType):
    def get_col_spec(self):
        return "[sys].[geometry]"

# Assuming PrintLogger is correctly implemented
from ..logger.default_logger import PrintLogger

def create_table_in_sqldb(engine, table_name, schema, column_names, column_types=None, primary_keys=None, default_type=NVARCHAR(None), default_primary=NVARCHAR(50), logger=PrintLogger()):
    """
    Creates a table in a SQL database using SQLAlchemy, with support for custom geometry data type.

    This function allows for dynamic creation of database tables with specified columns and data types,
    including a custom type for handling SQL Server's geometry data type.

    Args:
        engine: SQLAlchemy engine object. Represents the database connection where the table will be created.
        table_name: str. Name of the table to be created.
        schema: str. Database schema in which the table is to be created.
        column_names: list of str. Names of the columns to be included in the table.
        column_types: dict, optional. Mapping of column names to SQLAlchemy data types. If not provided, 
            all columns will use the default data type.
        primary_keys: list of str, optional. Names of columns that should be set as primary keys.
        default_type: SQLAlchemy data type, optional. Default data type to be used for columns 
            not specified in column_types. Defaults to NVARCHAR.
        logger: Logger object, optional. Logger for recording messages during the table creation process.

    Returns:
        None. The function creates a table in the database but does not return any value.
    """
    # Initialize metadata object
    metadata = MetaData()

    # Define columns for the table
    columns = []
    for name in column_names:
        # Check if the column is a primary key and set type to type specified
        if primary_keys and name in primary_keys:
            logger.info(f"Primary key detected setting to {default_primary}")
            col_type = default_primary
        # Determine the column type
        elif  column_types and name in column_types:
            if name == 'geometry':
                # Use custom SysGeometry type for the geometry column
                logger.info(f"Geometry detected, setting custom geometry data type")
                col_type = SysGeometry()
            else:
                col_type = column_types[name]
        else:
            col_type = default_type

        # Define the column
        columns.append(Column(name, col_type, primary_key=name in primary_keys if primary_keys else False))

    # Define the table with schema
    table = Table(table_name, metadata, *columns, schema=schema)

    try:
        # Create the table in the database
        metadata.create_all(engine)
        logger.info(f"Table '{table_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise

    return None
    

def create_table_in_pgdb(engine, table_name, schema, column_names, column_types=None, primary_keys=None, default_type=TEXT, default_primary=TEXT(50), logger=PrintLogger()):
    """
    Creates a table in a PostgreSQL database using SQLAlchemy and GeoAlchemy2, with support for GIS data types.

    This function allows for dynamic creation of database tables with specified columns and data types,
    including support for PostGIS's GEOMETRY data type.

    Args:
        engine: SQLAlchemy engine object. Represents the database connection where the table will be created.
        table_name: str. Name of the table to be created.
        schema: str. Database schema in which the table is to be created.
        column_names: list of str. Names of the columns to be included in the table.
        column_types: dict, optional. Mapping of column names to SQLAlchemy/GeoAlchemy2 data types. 
            If not provided, all columns will use the default data type.
        primary_keys: list of str, optional. Names of columns that should be set as primary keys.
        default_type: SQLAlchemy data type, optional. Default data type to be used for columns 
            not specified in column_types. Defaults to TEXT in PostgreSQL.
        logger: Logger object, optional. Logger for recording messages during the table creation process.

    Returns:
        None. The function creates a table in the database but does not return any value.
    """
    # Initialize metadata object
    metadata = MetaData()

    # Define columns for the table
    columns = []
    for name in column_names:
        # Check if the column is a primary key and set type to type specified
        if primary_keys and name in primary_keys:
            logger.info(f"Primary key detected setting to {default_primary}")
            col_type = default_primary
        # Determine the column type
        elif column_types and name in column_types:
            col_type = column_types[name]
        else:
            col_type = default_type

        # Define the column
        columns.append(Column(name, col_type, primary_key=name in primary_keys if primary_keys else False))

    # Define the table with schema
    table = Table(table_name, metadata, *columns, schema=schema)

    try:
        # Create the table in the database
        metadata.create_all(engine)
        logger.info(f"Table '{table_name}' created successfully in PostGIS database.")
    except Exception as e:
        logger.error(f"Error creating table in PostGIS database: {e}")
        raise

    return None