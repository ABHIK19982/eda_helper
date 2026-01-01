from fastapi import FastAPI
import uvicorn
from utils.helpers import *
import json
from utils.DataModel import DataModel, DataFile

config = read_config('config/app_conf.ini')
app = FastAPI(debug = config.get('COMMON', 'debug') == 'Y',
              title = config.get('COMMON','title'),
              version = config.get('COMMON','version'),
              description = config.get('COMMON','description'))

datamodellist: dict[int,DataModel]= {}
filelist: dict[int,DataFile] = {}
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/files/{file_id}", name = 'Load and parse the content of a file')
def upload_file(file_id: int, file: DataFile):
    try:
        filelist[file_id] = file
        datamodellist[file_id] = DataModel(file = file)
        return {'status_code': 200 , 'message': 'File loaded and parsed successfully'}
    except Exception as e:
        return {'status_code': 500, 'error_type': e.__class__.__name__,'error': str(e)}

@app.get("/files/list_files",name = 'List all the files loaded')
def list_files():
    files = {}
    for file_id in filelist.keys():
        files[file_id] = filelist[file_id].filename
    return {'status_code': 200, 'file list': files}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
