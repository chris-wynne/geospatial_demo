import re
import pandas as pd
import geopandas as gpd
from sqlalchemy import Integer, Float, String, DateTime, LargeBinary, NVARCHAR, Text, TIMESTAMP, Boolean, Date, Time, Numeric, Interval
from geoalchemy2 import Geometry
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from shapely.wkt import loads as load_wkt


from ..logger.default_logger import PrintLogger

def map_dataframe_dtypes_to_azure_ms_sql(df, logger=PrintLogger()):
    """
    Maps DataFrame dtypes to Azure SQL Server types, including geometry.

    Args:
        df: Pandas DataFrame.
    Return: 
        Dictionary with column names as keys and Azure SQL Server data types as values.
    """
    
    dtype_map = {
        'int64': Integer,
        'float64': Float,
        'object': NVARCHAR,
        'datetime64[ns]': DateTime,
        'bool': Integer,  # SQL Server doesn't have a boolean type, often mapped to int
        # Add other data types as needed
    }

    # Special handling for geometry data type
    # Assuming geometry data is stored in 'geometry' column in GeoDataFrame
    # GeoPandas is used for handling geometric data in DataFrames
    if 'geometry' in df.columns:
        logger.info(f"geometry data type detected")
        dtype_map['geometry'] = Geometry

    sql_dtypes = {}
    for col in df.columns:
        pandas_dtype = str(df[col].dtype)
        sql_dtype = dtype_map.get(pandas_dtype, String)  # Default to String if dtype not found
        sql_dtypes[col] = sql_dtype

    return sql_dtypes


def map_dataframe_dtypes_to_sqlalchemy(df, logger=PrintLogger()):
    """
    Maps DataFrame dtypes directly to SQLAlchemy or GeoAlchemy2 types. Handles both geometric types in GeoPandas GeoDataFrame
    and potential WKT geometry stored as strings in a pandas DataFrame.

    Args:
        df: Pandas DataFrame or GeoPandas GeoDataFrame.

    Return: 
        Dictionary with column names as keys and SQLAlchemy/GeoAlchemy2 data types as values.
    """

    dtype_map = {
        'int64': Integer,
        'int32': Integer,
        'float64': Float,
        'float32': Float,
        'object': Text,
        'datetime64[ns]': TIMESTAMP,
        'bool': Boolean,
        'timedelta[ns]': Interval,
        'datetime64[ns, tz]': TIMESTAMP(timezone=True),
        'date': Date,
        'time': Time,
        'category': String,
        'string': Text, 
        'bytes': LargeBinary,
        'UInt8': Integer,
        'UInt16': Integer,
        'UInt32': Integer,
        'UInt64': Integer,
        'Int8': Integer,
        'Int16': Integer,
        'Int32': Integer,
        'Int64': Integer,
        'float16': Float, 
        'complex': String,
        'decimal': Numeric,
    }

    sqlalchemy_dtypes = {}
    for col in df.columns:
        pandas_dtype = str(df[col].dtype)
        
        if pandas_dtype == 'object' and is_wkt_geometry(df[col], logger=logger):
            logger.info(f"Column '{col}' contains WKT-formatted strings, mapping to Geometry.")
            # Column contains WKT-formatted strings
            sqlalchemy_dtypes[col] = Geometry
        elif hasattr(df, 'geometry') and col == df.geometry.name:
            logger.info(f"Column '{col}' is identified as GeoDataFrame geometry column, mapping to Geometry.")
            # GeoDataFrame geometry column
            sqlalchemy_dtypes[col] = Geometry
        else:
            # Other non-spatial data types
            mapped_type = dtype_map.get(pandas_dtype, Text)  # Default to Text if dtype not found
            logger.info(f"Mapping column '{col}' with pandas dtype '{pandas_dtype}' to {mapped_type}.")
            sqlalchemy_dtypes[col] = mapped_type

    return sqlalchemy_dtypes


def is_wkt_geometry(series, logger=PrintLogger()):
    """
    Checks if a pandas Series contains WKT-formatted strings.
    
    Args:
        series (pd.Series): The pandas Series to check.
    
    Returns:
        bool: True if the series contains WKT geometries, False otherwise.
    """
    # Sample a few non-null values to check for WKT pattern
    sample_values = series.dropna().head(5)
    
    # Basic WKT patterns
    wkt_patterns = ['POINT', 'LINESTRING', 'POLYGON', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']
    
    for value in sample_values:
        if any(value.startswith(pattern) for pattern in wkt_patterns):
            logger.info(f"Detected WKT pattern in value.")
            return True
    logger.info("No WKT patterns detected in sampled values.")
    return False