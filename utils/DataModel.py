from pydantic import BaseModel, Field
from typing import Union, Optional, TextIO, Any
import pandas as pd


class DataFile(BaseModel):
    filename: str = Field(alias='Data File name',
                          description='The name of the file provided')
    file_type: str = Field(alias='Data file type',
                           description='The file type of the file provided')
    file_path: str = Field(alias='Data file path',
                           description='The path of the file provided')


class DataModel():
    __file_size__: Optional[int] = Field(default=None, alias='Data file size',
                                         description='The size of the file provided')
    __raw_file_content__: Optional[Union[int, str]] = Field(default=None, alias='Data file content',
                                                            description='The raw content of the file without any '
                                                                        'formatting')
    __formatted_file_content__: Union[pd.DataFrame, dict[str, pd.DataFrame], dict[Any, pd.DataFrame], None] = Field(
        default=None, alias='Data file content',
        description='The formatted content of the file')

    def __init__(self, **data):
        if 'file' not in data:
            raise ValueError("File Object not provided")
        f = data['file']
        self.__file = f
        if not isinstance(f, DataFile):
            raise ValueError("Invalid file provided. building a Datamodel requires a proper file of Datafile object")
        with open(f.file_path, 'r') as file:
            self.__file_size__ = file.__sizeof__()
            self.__raw_file_content__ = file.read()
            self.__formatted_file_content__ = None

    @property
    def file(self):
        return self.__file

    @property
    def file_size(self):
        return self.__file_size__

    @file_size.setter
    def file_size(self, fsize):
        self.__file_size__ = fsize

    @property
    def raw_file_content(self):
        return self.__raw_file_content__

    @raw_file_content.setter
    def raw_file_content(self, cont):
        self.__raw_file_content__ = cont

    @property
    def formatted_file_content(self):
        return self.__formatted_file_content__

    @formatted_file_content.setter
    def formatted_file_content(self, content):
        self.__formatted_file_content__ = content

    def load_formatted_content(self):
        if self.__file.file_type == 'csv':
            self.__formatted_file_content__ = pd.read_csv(self.__file.file_path)
        elif self.__file.file_type == 'json':
            self.__formatted_file_content__ = pd.read_json(self.__file.file_path)
        elif self.__file.file_type == 'excel':
            self.__formatted_file_content__ = pd.read_excel(self.__file.file_path, sheet_name=None)
        else:
            raise ValueError("Invalid file type provided. Only csv, json, and excel are supported")
