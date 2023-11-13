from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Any

Base = declarative_base() #type:Any


class IPTable(Base):
    """
    Represents an IP address entry in the database.
    """

    __tablename__ = "ip_addresses"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"))
    data_source = relationship("DataSource", back_populates="ip_addresses")


class URLTable(Base):
    """
    Represents a URL address entry in the database.
    """

    __tablename__ = "url_addresses"
    id = Column(Integer, primary_key=True)
    url_address = Column(String, unique=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"))
    data_source = relationship("DataSource", back_populates="url_addresses")


class DataSource(Base):
    """
    Represents a data source in the database.
    """

    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    ip_addresses = relationship("IPTable", back_populates="data_source")
    url_addresses = relationship("URLTable", back_populates="data_source")
