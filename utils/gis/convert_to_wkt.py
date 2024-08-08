import geopandas as gpd
import binascii
from shapely import wkb
from ..logger.default_logger import PrintLogger

def convert_geometry_type_to_wkt(gdf, column="geometry", logger=PrintLogger()):
    """
    Convert the geometry column of a GeoDataFrame to Well-Known Text (WKT) format.

    This function takes a GeoDataFrame and converts the specified geometry column
    to WKT format. The original geometry column is dropped, and a new column with
    the same name as the original one is created to store the converted WKT geometries.

    Args:
        gdf (geopandas.GeoDataFrame): The GeoDataFrame to convert.
        column (str, optional): The name of the geometry column to convert (default is "geometry").
        logger (object, optional): An instance of a logger to record information and errors (default is PrintLogger()).

    Returns:
        geopandas.GeoDataFrame: A new GeoDataFrame with the geometry column converted to WKT,
        or the original GeoDataFrame if an error occurs during conversion.
    """
    logger.info(f"Converting {column} to WKT format")
    try:
        converted_gdf = gdf.copy()
        converted_gdf['wkt'] = converted_gdf[column].to_wkt()
        converted_gdf = converted_gdf.drop(column, axis=1) # Drop the column 'old_column'
        converted_gdf = converted_gdf.rename(columns={'wkt': column}) # Rename 'current_column' to 'new_column'
        logger.info(f"Converted to WKT")
        
    except Exception as e:
        logger.error(f"Error converting to WKT: {e}")
        return gdf

    return converted_gdf


def hex_to_wkb(hex_str):
    """
    Convert a hexadecimal string representation of WKB (Well-Known Binary) to its binary form.

    Args:
        hex_str (str): The hexadecimal string representation of a WKB geometry.

    Returns:
        bytes: The binary representation of the WKB geometry.

    Raises:
        binascii.Error: If `hex_str` cannot be converted due to improper formatting.
    """
    try:
        wkb_bytes = binascii.unhexlify(hex_str)
        return wkb_bytes
    except binascii.Error as e:
        raise

def convert_wkb_column_to_geometries(df, wkb_column='geometry', logger=PrintLogger()):
    """
    Convert a DataFrame column containing hexadecimal string representations of WKB geometries 
    to `shapely` geometry objects.

    This function applies the conversion to each entry in the specified column of the DataFrame 
    and replaces the original hexadecimal strings with their corresponding `shapely` geometry objects.

    Args:
        df (pandas.DataFrame): The DataFrame containing the WKB hexadecimal strings.
        wkb_column (str, optional): The name of the column containing the WKB hex strings. Defaults to 'geometry'.

    Returns:
        pandas.DataFrame: The DataFrame with the specified column converted to `shapely` geometry objects.

    Raises:
        Exception: If any error occurs during the conversion process.
    """
    try:
        df[wkb_column] = df[wkb_column].apply(lambda x: wkb.loads(hex_to_wkb(x)))
        logger.info(f"Successfully converted column '{wkb_column}' to geometry objects.")
    except Exception as e:
        logger.error(f"Error converting column '{wkb_column}' to geometry objects: {e}")
        raise
    return df
