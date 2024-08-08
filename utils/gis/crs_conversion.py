import geopandas as gpd

from ..logger.default_logger import PrintLogger

def ensure_crs(gdf, desired_crs="EPSG:4326", logger=PrintLogger()):
    """
    Checks the CRS (Coordinate Reference System) of a GeoDataFrame and converts it to the desired CRS if they don't match.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame whose CRS is to be checked.
        desired_crs (str or dict): The desired CRS to which the GeoDataFrame should be converted if necessary. 
                               This can be a string like 'EPSG:4326' or a PROJ4 string.

    Returns:
        GeoDataFrame: A GeoDataFrame with the desired CRS.
    """
    if gdf.crs is None:
        logger.error("The GeoDataFrame has no CRS defined.")
        raise ValueError("The GeoDataFrame has no CRS defined.")

    # Check if the current CRS matches the desired CRS
    if gdf.crs.to_string() != desired_crs:
        # Convert the GeoDataFrame to the desired CRS
        old_crs = gdf.crs
        gdf = gdf.to_crs(desired_crs)
        logger.info(f"CRS converted to {desired_crs} from {old_crs}.")
    else:
        logger.info(f"CRS already matches the desired CRS: {desired_crs}.")

    return gdf