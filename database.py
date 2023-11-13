from sqlalchemy import create_engine, Column
import configparser
from models import Base
from sqlalchemy.orm import sessionmaker
from models import IPTable, URLTable, DataSource
from sqlalchemy import Column

config = configparser.ConfigParser()
config.read("config.ini")

host = config.get("Database", "host")
username = config.get("Database", "username")
password = config.get("Database", "password")
database = config.get("Database", "database")

engine = create_engine(f"postgresql://{username}:{password}@{host}/{database}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def save_url_csv(item: str, data_source_id: Column[int]) -> None:
    """
    Saves a URL to the database in CSV format.

    :param item: The URL you want to save.
    :param data_source_id: The ID of the data source associated with the URL.
    :return: None
    """
    url_entry = URLTable(url_address=str(item), data_source_id=data_source_id)
    session.add(url_entry)
    session.commit()


def save_url_text(line: str, data_source_id: Column[int]) -> None:
    """
    Saves a URL to the database in plain text format.

    :param line: The URL you want to save.
    :param data_source_id: The ID of the data source associated with the URL.
    :return: None
    """
    url_entry = URLTable(url_address=str(line), data_source_id=data_source_id)
    session.add(url_entry)
    session.commit()


def save_ip(ip_address: str, data_source_id: Column[int]) -> None:
    """
    Saves an IP address to the database.

    :param ip: The IP address you want to save.
    :param data_source_id: The ID of the data source associated with the IP address.
    :return: None
    """
    ip_entry = IPTable(ip_address=str(ip_address), data_source_id=data_source_id)
    session.add(ip_entry)
    session.commit()


def save_source(source: str) -> DataSource:
    """
    Saves a data source to the database.

    :param source: The URL of the data source you want to save.
    :return: An instance of DataSource representing the data source.
    """
    data_source = DataSource(url=source)
    session.add(data_source)
    session.commit()
    return data_source


def check_existing(model: type, column: Column[str], value: str) -> DataSource:
    """
    Checks the existence of a record in the database.

    :param model: The model class in which you want to check the existence of a record.
    :param column: The column where you're checking the value.
    :param value: The value you want to check.
    :return: An existing record if it exists, otherwise None.
    """
    existing_entry = session.query(model).filter(column == str(value)).first()
    return existing_entry
