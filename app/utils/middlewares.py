import functools

from flask import request

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if request.headers.get('Authorization', None):
            return view(*args, **kwargs)
        else:
            return "APi failed"
    
    return wrapped_view