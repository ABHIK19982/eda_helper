from configparser import RawConfigParser
from typing import TextIO, Union
import nbformat as nbf
import json
from utils.DataModel import DataFile
from utils.exceptions.custom_exceptions import FileIdNotFoundError, FileAlreadyExistsError
from utils.notebook_template import *
from sqlalchemy import create_engine, text
from sqlalchemy import URL


def read_config(file_path: Union[str, TextIO]):
    config = RawConfigParser()
    config.read(file_path)
    return config


def create_notebook(dt_file, nb_prefix):
    conf = read_config('config/app_conf.ini')
    pd = dt_file.formatted_file_content
    nb = nbf.v4.new_notebook()
    top_cell = nbf.v4.new_code_cell(TOP_LEVEL_CELL)
    top_mkd_cell = nbf.v4.new_markdown_cell(LOAD_MARKDOWN_CELL)
    load_cell = nbf.v4.new_code_cell(
        LOAD_DATA_CODE_DELL.format(FILE_TYPE=dt_file.file.file_type, FILE_PATH=dt_file.file.file_path))
    mkd_cell = nbf.v4.new_markdown_cell(EDA_MKD_CELL)
    desc_cell = nbf.v4.new_code_cell(DESCRIBE_DATA_CODE_CELL)
    nb['cells'] = [top_cell, top_mkd_cell, load_cell, mkd_cell, desc_cell]
    for col in pd.columns:
        if pd[col].dtype == 'object':
            mkd_ell = nbf.v4.new_markdown_cell(ANALYSIS_MKD_CELL.format(COL=col))
            cd_cell = nbf.v4.new_code_cell(OBJECT_DATA_EDA_CODE_CELL.format(COL=col))
        else:
            mkd_ell = nbf.v4.new_markdown_cell(ANALYSIS_MKD_CELL.format(COL=col))
            cd_cell = nbf.v4.new_code_cell(NUMERICAL_DATA_EDA_CODE_CELL.format(COL=col))
        nb['cells'].append(mkd_ell)
        nb['cells'].append(cd_cell)
    print('writing notebook')
    notebook_prefix = f"{conf.get('NOTEBOOK', 'prefix', fallback='')}{dt_file.file.filename.split('.')[0] if nb_prefix is None else nb_prefix}"
    with open(
            f"{conf.get('NOTEBOOK', 'loc')}/{notebook_prefix}{conf.get('NOTEBOOK', 'suffix', fallback='')}.ipynb",
            'w+') as f:
        nbf.write(nb, f)
    print('notebook write complete ')


def read_files_from_store_by_fileid(file_id: str):
    config = read_config('config/app_conf.ini')
    url_object = URL.create(
        "mysql",
        username=config.get('DATABASE', 'username'),
        password=config.get('DATABASE', 'password'),  # plain (unescaped) text
        host=config.get('DATABASE', 'host'),
        database=config.get('DATABASE', 'database'),
    )
    with create_engine(url = url_object).connect() as conn:
        result = conn.execute(text(f"select * from {config.get('DATABASE','file_store_name')} where file_id = :file_id"),
                     [{"file_id" : file_id}])

    if result.rowcount == 0:
        raise FileIdNotFoundError(file_id)
    else:
        res = list(result.mappings())[0]
        return DataFile.model_validate(res , by_name = True)

def check_file_id_exist(filename : str):
    config = read_config('config/app_conf.ini')
    url_object = URL.create(
        "mysql",
        username=config.get('DATABASE', 'username'),
        password=config.get('DATABASE', 'password'),  # plain (unescaped) text
        host=config.get('DATABASE', 'host'),
        database=config.get('DATABASE', 'database'),
    )
    with create_engine(url=url_object).connect() as conn:
        result = conn.execute(
            text(f"select count(*) from {config.get('DATABASE', 'file_store_name')} where filename = :filename"),
            [{"filename": filename.lower()}]).first()

    return bool(result.tuple()[0])

def get_highest_file_id():
    config = read_config('config/app_conf.ini')
    url_object = URL.create(
        "mysql",
        username=config.get('DATABASE', 'username'),
        password=config.get('DATABASE', 'password'),
        host=config.get('DATABASE', 'host'),
        database=config.get('DATABASE', 'database'),
    )
    with create_engine(url=url_object).connect() as conn:
        result = conn.execute(
            text(f"select max(file_id) from {config.get('DATABASE', 'file_store_name')}")).first().tuple()[0]
    print(result)
    return result if result is not None else 0

def read_files_from_store():
    config = read_config('config/app_conf.ini')
    url_object = URL.create(
        "mysql",
        username=config.get('DATABASE', 'username'),
        password=config.get('DATABASE', 'password'),  # plain (unescaped) text
        host=config.get('DATABASE', 'host'),
        database=config.get('DATABASE', 'database'),
    )
    with create_engine(url=url_object).connect() as conn:
        result = conn.execute(text(f"select * from {config.get('DATABASE', 'file_store_name')}"))
    return {res.file_id: DataFile.model_validate(res, by_name=True) for res in result.mappings()}

def write_files_into_store(file_id:str, dfile:DataFile):
    config = read_config('config/app_conf.ini')
    url_object = URL.create(
        "mysql",
        username=config.get('DATABASE', 'username'),
        password=config.get('DATABASE', 'password'),  # plain (unescaped) text
        host=config.get('DATABASE', 'host'),
        database=config.get('DATABASE', 'database'),
    )
    check_file = check_file_id_exist(dfile.filename)
    if check_file :
        raise FileAlreadyExistsError(file_id)

    with create_engine(url=url_object).connect() as conn:
        result = conn.execute(
            text(f"insert into {config.get('DATABASE', 'file_store_name')} values (:fileid, :filename, :filetype, "
                 f":filepath)"),
            [{"fileid": file_id,
              "filename": dfile.filename,
              "filetype": dfile.file_type,
              "filepath": dfile.file_path}])
        conn.commit()
