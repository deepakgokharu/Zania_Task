import json
import os
from http import HTTPStatus
from werkzeug.utils import secure_filename
from flask import current_app

from ..utils.utility_functions import (
    create_response, get_new_uuid, is_file_allowed
)
from .llm_model import get_model_from_document

def get_answers(questions_file, document_file):
    try:

        # initialising the document and questions file path with empty value
        document_file_path = None
        questions_file_path = None
        # checking for file validaions
        
        if not is_file_allowed(questions_file) or not is_file_allowed(document_file):
            raise Exception('Either file is not sent or file is corrupted.')

        
        # saving the file to server, so we can pass the file address to model, which will make it more decoupled and scalable
        questions_filename = get_new_uuid()+questions_file.filename
        questions_file.save(os.path.join(current_app.instance_path, secure_filename(questions_filename)))
        questions_file_path = os.path.join(current_app.instance_path, secure_filename(questions_filename))
        
        document_filename = get_new_uuid()+document_file.filename
        document_file.save(os.path.join(current_app.instance_path, secure_filename(document_filename)))
        document_file_path = os.path.join(current_app.instance_path, secure_filename(document_filename))

        rag_chain, error = get_model_from_document(document_file_path)

        if error is None:
            resp = {}
            
            with open(questions_file_path, 'r') as questions_data:
                questions = json.load(questions_data)
                for question in questions:
                    resp[question] = rag_chain.invoke(question)
        else:
            raise Exception(str(error))

        # deleting the file afterwards
        # deleting the files, if they are not deleted
        if document_file_path is not None:
            os.remove(document_file_path)
        if questions_file_path is not None:
            os.remove(questions_file_path)
        return resp
    except Exception as e:

        # deleting the files, if they are not deleted
        if document_file_path is not None:
            os.remove(document_file_path)
        if questions_file_path is not None:
            os.remove(questions_file_path)

        return create_response(HTTPStatus.INTERNAL_SERVER_ERROR.value, '', str(e))