import os

from fastapi import FastAPI
import uvicorn
from utils.helpers import *
from utils.exceptions.custom_exceptions import (InvalidFileTypeError,
                                                FilePathNotFoundError,
                                                FileTypeNotMatchingError,
                                                FileNameNotProvidedError,
                                                FileIdNotFoundError)
from utils.DataModel import DataModel, DataFile

config = read_config('config/app_conf.ini')
app = FastAPI(debug=config.get('COMMON', 'debug') == 'Y',
              title=config.get('COMMON', 'title'),
              version=config.get('COMMON', 'version'),
              description=config.get('COMMON', 'description'))

datamodellist: dict[int, DataModel] = {}
filelist: dict[int, DataFile] = {}


@app.post("/files/{file_id}", name='Load and parse the content of a file')
def upload_file(file_id: int, file: DataFile):
    try:
        if file.file_type not in ('csv', 'json', 'xlsx'):
            raise InvalidFileTypeError(file.file_type)

        if file.file_path == '':
            raise FilePathNotFoundError()
        elif file.file_path != '' and not os.path.exists(file.file_path):
            raise FileNotFoundError(file.file_path)

        if file.filename == '':
            raise FileNameNotProvidedError()
        elif file.filename.split('.')[-1] != file.file_type:
            raise FileTypeNotMatchingError(file.file_type, file.filename.split('.')[-1])

        filelist[file_id] = file
        datamodellist[file_id] = DataModel(file=file)
        datamodellist[file_id].load_formatted_content()
        return {'status_code': 200, 'message': 'File loaded and parsed successfully'}
    except Exception as e:
        return {'status_code': 500, 'error_type': e.__class__.__name__, 'error': str(e)}


@app.get("/files/list_files", name='List all the files loaded')
def list_files():
    files = {}
    for file_id in filelist.keys():
        files[file_id] = filelist[file_id].filename
    return {'status_code': 200, 'file list': files}


@app.get("/data/{file_id}/columns", name='List all the columns in a file')
def get_columns_by_fileid(file_id: int):
    try:
        if file_id not in filelist.keys():
            raise FileIdNotFoundError(file_id)
        return {'status_code': 200, 'columns': datamodellist[file_id].formatted_file_content.columns.tolist()}
    except Exception as e:
        return {'status_code': 500, 'error_type': e.__class__.__name__, 'error': str(e)}


@app.get("/notebook/{file_id}/create", name='Create a notebook for a file')
def create_notebook_by_id(file_id: int, notebook_prefix: str):
    try:
        if file_id not in filelist.keys():
            raise FileIdNotFoundError(file_id)
        create_notebook(datamodellist[file_id], notebook_prefix)
        return {'status_code': 200, 'message': 'Notebook created successfully'}
    except Exception as e:
        return {'status_code': 500, 'error_type': e.__class__.__name__, 'error': str(e)}


if __name__ == "__main__":
    filelist = read_files_from_store() if os.path.exists(
        read_config('config/app_conf.ini').get('STORE', 'store_loc')) else {}
    for fileid in filelist.keys():
        datamodellist[fileid] = DataModel(file=filelist[fileid])
        datamodellist[fileid].load_formatted_content()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    write_files_into_store(filelist)
