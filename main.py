from fastapi import FastAPI
import uvicorn

from api_utils.data_func import get_columns_by_fileid
from api_utils.notebook_func import create_notebook_by_id
from utils.helpers import *
from api_utils.files_func import *

config = read_config('config/app_conf.ini')
app = FastAPI(debug=config.get('COMMON', 'debug') == 'Y',
              title=config.get('COMMON', 'title'),
              version=config.get('COMMON', 'version'),
              description=config.get('COMMON', 'description'))
app.post("/files/load")(upload_file)
app.get("/files/list")(list_files)
app.get("/data/{file_id}/columns")(get_columns_by_fileid)
app.get("/notebook/{file_id}/create")(create_notebook_by_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
