import requests
import json
import logging
from json.decoder import JSONDecodeError
from data_processing import ip_url_validator
from database import save_source, check_existing
from models import DataSource

# - Log record format includes timestamp, log level, and the message.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    """
    Process data sources from a configuration file.

    Loads data sources from a configuration file, checks for existing sources in the database,
    and retrieves or logs errors for each source.

    Raises:
        Exception: If there's an error while loading the configuration file.

    Returns:
        None
    """
    try:
        with open("source.json", "r") as source_file:
            source_url = json.load(source_file)
              
        sources = source_url["data_sources"]
        if not sources:
            raise ValueError("The 'data_sources' key is empty.")       
        for source in sources:
            data_source = process_data_source(source)
            try:
                response = requests.get(source)
                if response.status_code == 200:
                    ip_url_validator(response, data_source.id)
                else:
                    logging.info("Error while downloading data.")
            except ConnectionError as connection_e:
                logging.error(f"Error connecting to the server: {connection_e}")
    except KeyError as key_error:
        logging.info(f"KeyError: {key_error}")
    except JSONDecodeError as json_error:
        logging.info(f"Error decoding JSON data: {json_error}")
    except ValueError as value_error:
        logging.info(f"Invalid configuration: {value_error}")
    except FileNotFoundError as file_error:
        logging.info(f"Error when loading the configuration file: {file_error}")


def process_data_source(source: str) -> DataSource:
    """
    Process a data source, checking if it already exists in the database. If it does, return the existing
    DataSource instance. If it doesn't, create a new DataSource instance and return it.

    :param source: The URL of the data source to be processed.
    :type source: str

    :return: The DataSource instance corresponding to the data source.
    :rtype: DataSource
    """

    existing_url_entry = check_existing(DataSource, DataSource.url, source)
    if existing_url_entry:
        return existing_url_entry 
    return save_source(source)

if __name__ == "__main__":
    main()


