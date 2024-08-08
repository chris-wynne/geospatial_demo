import io
import pandas as pd
import geopandas as gpd
import requests

from ..logger.default_logger import PrintLogger

def request_response_to_df(request_url, response_format='json', is_geospatial=False, params=None, headers=None, logger=PrintLogger()):
    """
    Send a request to a given URL and process the response based on the specified format.

    Args:
        request_url (str): The URL to send the request to.
        response_format (str, optional): The format of the expected response. Defaults to 'json'.
        is_geospatial (bool, optional): Whether the response contains geospatial data. Defaults to False.
        params (dict, optional): Parameters to include in the request. Defaults to None.
        auth_headers (dict, optional): Headers for authentication. Defaults to None.
        logger (PrintLogger, optional): Logger object to log messages. Defaults to PrintLogger().

    Returns:
        dict or pd.DataFrame or gpd.GeoDataFrame or None: Processed data from the response if successful, otherwise None.
            If response_format is 'json' and is_geospatial is True, returns a GeoDataFrame.
            If response_format is 'json' and is_geospatial is False, returns a DataFrame.
            If response_format is 'csv', returns a DataFrame.
    """
    try:
        response = requests.get(request_url, params=params, headers=headers)
        
        if response.status_code == 200:
            if response_format == 'json':
                # Process the response as JSON
                data = response.json()
                if is_geospatial:
                    # Convert the JSON data to a GeoDataFrame for geospatial data
                    data = gpd.GeoDataFrame.from_features(data['features'])
                else:
                    # Convert the JSON data to a DataFrame for normal data
                    data = pd.json_normalize(data)
            elif response_format == 'csv':
                # Process the response as CSV
                data = pd.read_csv(io.StringIO(response.text)) # Assuming the response content is text/csv
            else:
                logger.error(f"Unsupported response format: {response_format}")
                data = None
        else:
            logger.error("Failed to retrieve data", response.status_code)
            data = None
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        data = None

    return data