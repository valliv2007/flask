from functools import wraps

import flask
import werkzeug
import werkzeug.wrappers

def responce(*, mimetype: str = None, template_file:str = None):
    def responce_inner(res):

        @wraps(res)
        def view_method(*args, **kwargs):
            responce_val = res(*args, **kwargs)
            if isinstance(responce_val, werkzeug.wrappers.Response):
                return responce_val

            if isinstance(responce_val, flask.Response):
                return responce_val

            if isinstance(responce_val, dict):
                model = dict(responce_val)
            else:
                model = dict()

            if template_file and not isinstance(responce_val, dict):
                raise Exception('Invalid type of Responce')
            if template_file:
                responce_val = flask.render_template(template_file, **responce_val)

            resp = flask.make_response(responce_val)
            resp.model = model
            if mimetype:
                resp.mimetype = mimetype

            return resp

        return view_method
    return responce_inner
