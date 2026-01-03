class InvalidFileTypeError(Exception):
    def __init__(self, file_type):
        super().__init__(f"Invalid file type provided: {file_type}")
        self.__file_type = file_type

    def __repr__(self):
        return f"Invalid File Type provided: File type provided should be within the recommended set only  - csv,excel,json')"

class FilePathNotFoundError(Exception):
    def __init__(self):
        super().__init__("File path not provided")

    def __repr__(self):
        return f"File path not provided: File path should be provided for the file to be loaded"

class FileNameNotProvidedError(Exception):
    def __init__(self):
        super().__init__("File name not provided")

    def __repr__(self):
        return f"File name not provided: File name should be provided for the file to be loaded"

class FileTypeNotMatchingError(Exception):
    def __init__(self, file_type, org_file_type):
        super().__init__(f"File type not matching: {file_type} and {org_file_type}")
        self.__file_type = file_type
        self.__org_file_type = org_file_type

    def __repr__(self):
        return f"The file type provided and the actual file extensions are not matching - {self.__org_file_type} and {self.__file_type}"

class FileIdNotFoundError(Exception):
    def __init__(self, file_id):
        super().__init__(f"File ID not found: {file_id}")
        self.__file_id = file_id

    def __repr__(self):
        return f"The file ID provided is not found - {self.__file_id}"