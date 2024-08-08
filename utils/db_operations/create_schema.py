from sqlalchemy import create_engine, text

from ..logger.default_logger import PrintLogger

def ensure_schema_exists(engine, schema, logger=PrintLogger()):
    """
    Ensures that the specified schema exists in the database; creates it if it does not.

    Args:
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine connected to the database.
        schema (str): The name of the schema to check and create if necessary.
        logger (Logger): Logger for logging messages.
    """
    with engine.begin() as conn:  # Use engine.begin() to automatically commit or rollback
        # Check if the schema exists
        schema_exists_query = text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema")
        schema_exists = conn.execute(schema_exists_query, {'schema': schema}).fetchone()

        # If the schema does not exist, create it
        if not schema_exists:
            conn.execute(text(f"CREATE SCHEMA \"{schema}\""))
            logger.info(f"Schema '{schema}' created.")
        else:
            logger.info(f"Schema '{schema}' already exists.")