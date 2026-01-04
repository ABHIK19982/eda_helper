import os
from utils.DataModel import DataFile
from utils.exceptions.custom_exceptions import InvalidFileTypeError, FilePathNotFoundError, FileNameNotProvidedError, \
    FileTypeNotMatchingError, FileAlreadyExistsError
from utils.helpers import check_file_id_exist, get_highest_file_id, write_files_into_store, read_files_from_store
from fastapi.responses import JSONResponse


def load_files_from_dir(file: DataFile):
    if not os.path.exists(file.file_path):
        raise FileNotFoundError(dir)

    if not os.path.isdir(file.file_path):
        raise NotADirectoryError(dir)

    file_paths = os.listdir(file.file_path)
    file_id = int(get_highest_file_id().split('-')[0]) + 1

    filelist = [{'file_id': file_id, 'filename': file.filename}]
    for cnt, file_path in enumerate(file_paths):
        if file_path.split('.')[-1] != file.file_type:
            raise FileTypeNotMatchingError(file.file_type, file_path.split('.')[-1])

        if check_file_id_exist(file.filename + '/' + file_path):
            raise FileAlreadyExistsError(file.filename + '/' + file_path)
        write_files_into_store(f"{file_id}-{cnt + 1}", DataFile.model_validate({"filename":file.filename + '/' + file_path,"file_type":file.file_type,"file_path":file.file_path + '/' + file_path}, by_name = True))
        filelist.append({'file_id': f"{file_id}-{cnt + 1}", 'filename': file.filename + '/' + file_path})
    write_files_into_store(f"{file_id}-0", file)
    return JSONResponse(status_code=200,
                        content={'message': 'File loaded successfully',
                                 'File details': filelist}
                        )


def upload_file(file: DataFile):
    try:
        if os.path.isdir(file.file_path):
            return load_files_from_dir(file)
        else:
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
            write_files_into_store(f"{file_id}-0", file)
            return JSONResponse(status_code=200,
                                content={'message': 'File loaded successfully',
                                         'File details': {'file_id': file_id, 'filename': file.filename}}
                                )
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={'error_type': e.__class__.__name__, 'error': str(e)}
                            )


def list_files():
    files = {}
    filelist = read_files_from_store()
    for file_id in filelist.keys():
        files[file_id] = filelist[file_id].filename
    return JSONResponse(status_code=200, content={'file list': files})
