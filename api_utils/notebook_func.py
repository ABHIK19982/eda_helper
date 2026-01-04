from utils.DataModel import DataModel
from utils.helpers import read_files_from_store_by_fileid, create_notebook
from fastapi.responses import JSONResponse

def create_notebook_by_id(file_id: str, notebook_prefix: str = None):
    try:
        dfile = read_files_from_store_by_fileid(file_id)
        datamodel = DataModel(file=dfile)
        datamodel.load_formatted_content()
        create_notebook(datamodel, notebook_prefix)
        return JSONResponse(status_code = 200, content = {'message': 'Notebook created successfully'})
    except Exception as e:
        return JSONResponse(status_code= 500, content = {'error_type': e.__class__.__name__, 'error': str(e)})