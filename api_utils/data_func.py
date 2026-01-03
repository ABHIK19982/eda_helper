from utils.DataModel import DataModel
from utils.helpers import read_files_from_store_by_fileid
from fastapi.responses import JSONResponse

def get_columns_by_fileid(file_id: int):
    try:
        dfile = read_files_from_store_by_fileid(file_id)
        datamodel = DataModel(file=dfile)
        datamodel.load_formatted_content()
        return JSONResponse(status_code= 200, content={'columns': datamodel.formatted_file_content.columns.tolist()})
    except Exception as e:
        return JSONResponse(status_code= 500, content = {'error_type': e.__class__.__name__, 'error': str(e)})
