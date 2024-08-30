import os
import json
import random

from .global_variables import (
    ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
)

def is_file_allowed(file):
    if not file or file.filename == '':
        return False
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return False
    
    return True

def check_file_size_parameters(file):
    # checking for file size and limiting it, if exeeds the limit
    file_length = file.seek(0, os.SEEK_END)

    if file_length > MAX_CONTENT_LENGTH:
        return False

    file.seek(0, os.SEEK_SET)
    # resetting the file seeking, so we can save it if we want to
    return True

def create_response(status, message='', error_message=''):
    return json.dumps({
            'status': status,
            'message': message,
            'error_message': error_message,
        })

def get_new_uuid():
    return str(random.randint(0, 1000000000))

def get_file_type(filename):
    return filename.rsplit('.', 1)[1].lower()