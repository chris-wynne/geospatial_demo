from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from ..logger.default_logger import PrintLogger

def clear_table_if_not_empty(engine, schema, table_name, logger=PrintLogger()):
    """
    Checks if a PostgreSQL table within a specified schema has any data and clears it if so, using an SQLAlchemy engine.

    Args:
        engine: SQLAlchemy engine object. Represents the database connection where the operation will be executed.
        schema: str. Name of the schema containing the table.
        table_name: str. Name of the table to check and potentially clear.
        logger: Logger object, optional. Logger for recording messages during the operation.

    Returns:
        bool: True if the table was cleared, False if the table was already empty.
    """
    try:
        with engine.connect() as conn:
            # Begin a transaction
            trans = conn.begin()
            
            # Check if the table has any data
            query_check = f"SELECT COUNT(*) FROM \"{schema}\".\"{table_name}\""
            result = conn.execute(text(query_check))
            count = result.scalar()
            
            if count > 0:
                # Clear the table if it has data
                query_delete = f"DELETE FROM \"{schema}\".\"{table_name}\""
                conn.execute(text(query_delete))
                trans.commit()  # Commit the transaction
                logger.info(f"Table '{schema}.{table_name}' cleared, {count} rows deleted.")
                return True
            else:
                logger.info(f"Table '{schema}.{table_name}' is already empty.")
                return False
    except SQLAlchemyError as e:
        logger.error(f"An error occurred during table clearing: {e}")
        if 'trans' in locals():
            trans.rollback()  # Rollback the transaction in case of error
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if 'trans' in locals():
            trans.rollback()
        return False

