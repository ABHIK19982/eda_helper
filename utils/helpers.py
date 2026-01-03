from configparser import RawConfigParser
from typing import TextIO, Union
import nbformat as nbf
import json
from utils.DataModel import DataFile
from utils.notebook_template import *


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


def read_files_from_store():
    config = read_config('config/app_conf.ini')
    files = {}
    j_data = json.load(open(config.get('STORE', 'store_loc'), 'r'))
    for file_id in j_data.keys():
        files[int(file_id)] = DataFile.model_validate_json(json.dumps(j_data[file_id]))
    return files


def write_files_into_store(files: dict[int, DataFile]):
    config = read_config('config/app_conf.ini')
    file_dict = {k: v.model_dump(by_alias=True) for k, v in files.items()}
    with open(config.get('STORE', 'store_loc'), 'w') as f:
        json.dump(file_dict, f, default=lambda o: o.__dict__, indent=4)
