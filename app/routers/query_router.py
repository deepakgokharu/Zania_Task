from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from http import HTTPStatus

from ..utils.global_variables import (
    POST, PUT, API_PATH
)
from ..utils.utility_functions import (
    create_response
)
from ..utils.middlewares import login_required
from ..controllers import query_controller

bp = Blueprint('queries', __name__, url_prefix=(API_PATH + '/queries'))


@bp.route('/get_answers', methods=[POST, PUT])
@login_required
def get_answers():
    # required when 2 types of method are allowed
    if request.method == POST:

        try:

            questions_file = request.files.get('questions', None)
            document_file = request.files.get('document', None)

            return query_controller.get_answers(questions_file, document_file)
                    
        
        
        except Exception as e:
            return create_response(HTTPStatus.INTERNAL_SERVER_ERROR.value, '', str(e))
    else:
        return create_response(HTTPStatus.METHOD_NOT_ALLOWED.value, '', 'Requested method not allowed')