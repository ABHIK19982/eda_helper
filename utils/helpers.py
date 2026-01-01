from configparser import RawConfigParser
from typing import Optional, TextIO, Union

from utils.DataModel import DataFile, DataModel


def read_config(file_path: Union[str, TextIO]):
    config = RawConfigParser()
    config.read(file_path)
    return config