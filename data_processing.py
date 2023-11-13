import csv
import logging
from requests import Response
from io import StringIO
from urllib.parse import urlparse
import ipaddress
from sqlalchemy import Column
from models import URLTable, IPTable
from database import (
    save_ip,
    save_url_csv,
    save_url_text,
    check_existing,
)





def processed_ip(line: str, data_source_id: Column[int]) -> None:
    """
    Process an IP address, checking for its existence in the database.

    This function takes a string containing an IP address and checks if it meets certain criteria.
    If the IP address is valid and not already present in the database, it is saved. If it already exists,
    its existence is logged.

    :param line: The string containing an IP address.
    :type line: str

    :param data_source_id: The ID of the data source associated with the processed data.
    :type data_source_id: int

    :return: None
    """

    parts = line.split("#")
    if len(parts) >= 8:
        slice_ip = parts[0]
        try:
            ip_adress = ipaddress.ip_address(slice_ip)
            existing_ip_entry = check_existing(IPTable, IPTable.ip_address, ip_adress)
            if existing_ip_entry:
                logging.info(f"Existing IP address in database: {ip_adress}")
            else:
                save_ip(ip_adress, data_source_id)
        except ValueError as error:
            logging.info(f"Error while processing IP address: {error}")


def processed_url_text(line: str, data_source_id: Column[int]) -> None:
    """
    Process a text line containing a URL, checking for its existence in the database.

    This function takes a text line and checks if it contains a URL by examining its scheme (http/https).
    If a URL is found, it checks if it already exists in the database. If it does, it logs its existence.
    If it doesn't exist, the URL is saved to the database.

    :param line: The text line containing a URL.
    :type line: str

    :param data_source_id: The ID of the data source associated with the processed data.
    :type data_source_id: int

    :return: None
    """

    if urlparse(line).scheme:
        existing_url_entry = check_existing(URLTable, URLTable.url_address, line)
        if existing_url_entry:
            logging.info(f"Existing URL address in database: {line}")
        else:
            save_url_text(line, data_source_id)


def processed_url_csv(line: str, data_source_id: Column[int]) -> None:
    """
    Process URL data from a CSV-formatted line, checking for existing entries in the database.

    This function takes a CSV-formatted line and processes it, looking for URLs within the line's items.
    For each URL, it checks if it already exists in the database. If it does, it logs its existence.
    If it doesn't exist, the URL is saved to the database.

    :param line: The CSV-formatted line containing URL data.
    :type line: str

    :param data_source_id: The ID of the data source associated with the processed data.
    :type data_source_id: int

    :return: None
    """

    with StringIO(line) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            for item in row:
                if urlparse(item).scheme:
                    existing_url_entry = check_existing(
                        URLTable, URLTable.url_address, item
                    )
                    if existing_url_entry:
                        logging.info(f"Existing URL address in database: {item}")
                    else:
                        save_url_csv(item, data_source_id)


def ip_url_validator(response: Response, data_source_id: Column[int]) -> None:
    """
    Validate and process IP and URL data from a given HTTP response.

    This function takes an HTTP response and splits its text content into lines.
    It then processes each line, determining if it's an IP address, a URL, or neither,
    and delegates the processing to the appropriate sub-functions.

    :param response: The HTTP response object containing the data to validate and process.
    :type response: Response

    :param data_source_id: The ID of the data source associated with the processed data.
    :type data_source_id: int

    :return: None
    """

    data = response.text
    lines = data.split("\n")

    for line in lines:
        if "http" not in line and "https" not in line:
            processed_ip(line, data_source_id)
        elif line.startswith("http://") or line.startswith("https://"):
            processed_url_text(line, data_source_id)
        else:
            processed_url_csv(line, data_source_id)
