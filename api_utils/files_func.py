import os
from utils.DataModel import DataFile
from utils.exceptions.custom_exceptions import InvalidFileTypeError, FilePathNotFoundError, FileNameNotProvidedError, \
    FileTypeNotMatchingError, FileAlreadyExistsError
from utils.helpers import check_file_id_exist, get_highest_file_id, write_files_into_store, read_files_from_store
from fastapi.responses import JSONResponse

def upload_file( file: DataFile):
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

        if check_file_id_exist(file.filename):
            raise FileAlreadyExistsError(file.filename)

        file_id = get_highest_file_id() + 1
        write_files_into_store(file_id, file)
        return JSONResponse(status_code = 200,
                            content = {'message': 'File loaded successfully', 'File details':{'file_id': file_id, 'filename': file.filename}}
                            )
    except Exception as e:
        return JSONResponse(status_code= 500,
                            content = {'error_type': e.__class__.__name__, 'error': str(e)}
                            )


def list_files():
    files = {}
    filelist = read_files_from_store()
    for file_id in filelist.keys():
        files[file_id] = filelist[file_id].filename
    return JSONResponse(status_code= 200, content = {'file list': files})
