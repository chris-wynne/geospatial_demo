import pyproj
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from shapely import geometry
from shapely.ops import transform, nearest_points
from functools import partial

from ..logger.default_logger import PrintLogger

def join_points_to_polygons(points_gdf, polygons_gdf, how="inner", predicate="within", logger=PrintLogger()):
    """
    Performs a spatial join between a GeoDataFrame of points and a GeoDataFrame of polygons. Each point is
    matched with a polygon it falls within, and the attributes of the polygon are merged into the point's attributes.

    Parameters:
    - points_gdf (GeoDataFrame): Contains the points to be joined.
    - polygons_gdf (GeoDataFrame): Contains the polygons to join with the points.
    - how (str, optional): Specifies the type of join to be performed. Defaults to "inner".
    - predicate (str, optional): Specifies the spatial operation to use for joining. Defaults to "within".

    Returns:
    - GeoDataFrame: A GeoDataFrame containing the joined points and polygons, with the points inheriting the attributes of the polygons they fall within.
    """
    logger.info("Starting join of points to polygons.")
    
    # Ensure that both GeoDataFrames are using the same CRS
    if points_gdf.crs != polygons_gdf.crs:
        logger.info("Adjusting CRS of points to match polygons.")
        points_gdf.to_crs(polygons_gdf.crs, inplace=True)

    # Perform the spatial join
    joined_gdf = gpd.sjoin(points_gdf, polygons_gdf, how=how, predicate=predicate)
    logger.info("Spatial join completed.")

    return joined_gdf


def join_polygons(polygons_gdf1, polygons_gdf2, how="inner", predicate='intersects', logger=PrintLogger()):
    """
    Joins two GeoDataFrames of polygons based on a specified spatial relationship. Attributes from the second
    GeoDataFrame are appended to the first based upon their spatial interaction as defined by the spatial operation parameter.

    Parameters:
    - polygons_gdf1 (GeoDataFrame): Contains the primary set of polygons.
    - polygons_gdf2 (GeoDataFrame): Contains the secondary set of polygons whose attributes are to be joined.
    - how (str, optional): Specifies the type of join to be performed. Defaults to "inner".
    - predicate (str): Defines the spatial operation (e.g., 'intersects', 'contains', 'within') to use for joining.

    Returns:
    - GeoDataFrame: A GeoDataFrame containing the first set of polygons enhanced with attributes from the second set based on the spatial relationship.
    """
    logger.info(f"Starting polygon to polygon join using {predicate} operation.")
    
    # Ensure that both GeoDataFrames are using the same CRS
    if polygons_gdf1.crs != polygons_gdf2.crs:
        logger.info("Adjusting CRS of the first polygon set to match the second.")
        polygons_gdf1.to_crs(polygons_gdf2.crs, inplace=True)

    # Perform the spatial join based on the specified spatial operation
    joined_gdf = gpd.sjoin(polygons_gdf1, polygons_gdf2, how=how, predicate=predicate)
    logger.info("Spatial join of polygons completed.")

    return joined_gdf


def find_nearest_and_distance(gdf1, gdf2, gdf1_id="fid", gdf2_id="fid", logger=PrintLogger()):
    """
    Calculates the nearest point in `gdf2` for each point in `gdf1` and measures the geodesic distance between them.
    
    This function is designed to work with geospatial data, where both input GeoDataFrames (`gdf1` and `gdf2`) contain
    geographic information. It identifies the nearest point in `gdf2` for each point in `gdf1`, computes the distance
    between these points in meters, and returns a GeoDataFrame containing the results with identifiers and geometries.
    
    Args:
        gdf1 (GeoDataFrame): The first GeoDataFrame containing points for which nearest counterparts in `gdf2` are sought.
        gdf2 (GeoDataFrame): The second GeoDataFrame containing points considered as potential nearest neighbors to points in `gdf1`.
        gdf1_id (str, optional): The column name in `gdf1` that serves as an identifier. Defaults to "fid".
        gdf2_id (str, optional): The column name in `gdf2` that serves as an identifier. Defaults to "fid".
        logger (Logger, optional): A logger for recording informational messages throughout the function's execution. Defaults to an instance of `PrintLogger`.
    
    Returns:
        GeoDataFrame: A GeoDataFrame containing the identifiers from both `gdf1` and `gdf2`, the geometry of points in `gdf1`,
                    the nearest geometry from `gdf2`, and the distance in meters between each point and its nearest neighbor.
    """
    logger.info("Initiating nearest point and distance calculation.")

    # Check and log the original Coordinate Reference System (CRS)
    original_crs = gdf1.crs
    logger.info(f"Original CRS for gdf1: {original_crs}")

    # Ensure the geometry columns are correctly set
    gdf1 = gdf1.set_geometry('geometry')
    gdf2 = gdf2.set_geometry('geometry')

    # Estimate and log a suitable UTM CRS based on the first geometry in gdf1
    utm_crs = gdf1.estimate_utm_crs()
    logger.info(f"Estimated UTM CRS: {utm_crs}")

    # Convert and log the conversion of both GeoDataFrames to the estimated UTM CRS
    gdf1_utm = gdf1.to_crs(utm_crs)
    gdf2_utm = gdf2.to_crs(utm_crs)
    logger.info("Converted gdf1 and gdf2 to UTM CRS for distance calculation.")

    # Initialize data collection
    data = []

    # Create Transformer instances for transforming geometries between CRSs
    transformer_to_utm = Transformer.from_crs(original_crs, utm_crs, always_xy=True)
    transformer_to_original = Transformer.from_crs(utm_crs, original_crs, always_xy=True)

    for index, row in gdf1_utm.iterrows():
        
        # Calculate distances to all points in gdf2_utm and find the minimum
        distances = gdf2_utm.geometry.apply(lambda geom: row.geometry.distance(geom))
        nearest_idx = distances.idxmin()

        # Extract the nearest geometry and distance
        nearest_geom_utm = gdf2_utm.geometry.loc[nearest_idx]
        distance = distances[nearest_idx]

        # Transform geometries back to the original CRS
        row_geom_original = transformer_to_original.transform(*row.geometry.coords[0])
        nearest_geom_original = transformer_to_original.transform(*nearest_geom_utm.coords[0])

        # Append results including identifiers and transformed geometries
        data.append({
            'gdf1_id': gdf1.loc[index, gdf1_id],
            'gdf2_id': gdf2.loc[nearest_idx, gdf2_id],
            'geometry': gpd.GeoSeries([geometry.Point(row_geom_original)], crs=original_crs)[0],
            'nearest_geometry': gpd.GeoSeries([geometry.Point(nearest_geom_original)], crs=original_crs)[0],
            'distance_meters': distance
        })

    # Log completion of the nearest point and distance calculation
    logger.info("Completed nearest point and distance calculation. Compiling results.")

    # Convert results to a GeoDataFrame with the original CRS
    results = gpd.GeoDataFrame(data, crs=original_crs)

    return results


def filter_intersecting_polygons(gdf1, gdf2):
    """
    Filters gdf1 to keep only polygons that intersect with any polygon in gdf2.
    
    Args:
        gdf1: GeoDataFrame containing the first set of polygons.
        gdf2: GeoDataFrame containing the second set of polygons.
    
    Returns:
        A new GeoDataFrame containing only the polygons from gdf1 that intersect with any polygon in gdf2.
    """
    # This will create a boolean mask where each element is True if the polygon in gdf1 intersects
    # with any polygon in gdf2, and False otherwise.
    intersects_mask = gdf1['geometry'].apply(lambda x: gdf2['geometry'].intersects(x).any())
    
    # Filter gdf1 using the mask to keep only intersecting polygons
    return gdf1[intersects_mask]