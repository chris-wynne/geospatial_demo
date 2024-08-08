class PrintLogger:
    """
    A simple logger class that prints log messages to the console.

    This class is intended as a replacement for standard logging
    when a full-fledged logging framework is not necessary.

    Args:
        info(message, *args): Prints an informational message prefixed with 'INFO:'. 
        error(message, *args): Prints an error message prefixed with 'ERROR:'. 
        debug(message, *args): Prints a debug message prefixed with 'DEBUG:'. 

    Example usage:
        logger = PrintLogger()
        logger.info("This is an informational message")
        logger.error("This is an error message %s", "with more detail")
        logger.debug("This is a debug message with two details: %s and %s", "detail1", "detail2")
    """
    def info(self, message, *args):
        if args:
            message = message % args
        print(f"INFO: {message}")

    def error(self, message, *args):
        if args:
            message = message % args
        print(f"ERROR: {message}")

    def debug(self, message, *args):
        if args:
            message = message % args
        print(f"DEBUG: {message}")