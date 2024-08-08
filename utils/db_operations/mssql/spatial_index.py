from sqlalchemy import create_engine
from sqlalchemy.sql import text

from ...logger.default_logger import PrintLogger

def create_spatial_index_uk_bounding(engine, schema, table_name, column_name="geometry", logger=PrintLogger()):
    """
    Creates a spatial index on the specified column of a table with a bounding box covering the UK.

    Args
        param engine: SQLAlchemy engine object.
        param schema: The schema name.
        param table_name: The table name.
        param column_name: The column name on which to create the spatial index.
    """
    index_name = f"Index_{table_name}_1"

    sql = text(f"""
    CREATE SPATIAL INDEX [{index_name}]
        ON [{schema}].[{table_name}] ([{column_name}])
        USING GEOMETRY_GRID
        WITH (
            BOUNDING_BOX = (XMAX = 2, XMIN = -9, YMAX = 61, YMIN = 49),
            GRIDS = (LEVEL_1 = MEDIUM, LEVEL_2 = MEDIUM, LEVEL_3 = MEDIUM, LEVEL_4 = MEDIUM)
        );
    """)
       
    try:
        logger.info(f"Creating spatial index for table: {table_name}")
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(sql)
            logger.info(f"Spatial index created")
    except Exception as e:
        logger.error(f"Failed to create spatial index: {e}", exc_info=True)
        
def create_spatial_index_world_bounding(engine, schema, table_name, column_name="geometry", logger=PrintLogger()):
    """
    Creates a spatial index on the specified column of a table with a bounding box covering the entire world.

    Args:
        param engine: SQLAlchemy engine object.
        param schema: The schema name.
        param table_name: The table name.
        param column_name: The column name on which to create the spatial index.
    """
    index_name = f"Index_{table_name}_1"

    sql = text(f"""
    CREATE SPATIAL INDEX [{index_name}]
        ON [{schema}].[{table_name}] ([{column_name}])
        USING GEOMETRY_GRID
        WITH (
            BOUNDING_BOX = (XMAX = 180, XMIN = -180, YMAX = 90, YMIN = -90),
            GRIDS = (LEVEL_1 = MEDIUM, LEVEL_2 = MEDIUM, LEVEL_3 = MEDIUM, LEVEL_4 = MEDIUM)
        );
    """)

    try:
        logger.info(f"Creating spatial index for table: {table_name}")
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(sql)
            logger.info(f"Spatial index created")
    except Exception as e:
        logger.error(f"Failed to create spatial index: {e}", exc_info=True)