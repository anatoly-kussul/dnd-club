import json
import logging
from functools import wraps

from jsonschema import Draft4Validator

from dnd_club.helpers import api_response

string_schema = {'type': 'string'}
float_schema = {'type': 'number'}
int_schema = {'type': 'integer'}
bool_schema = {'type': 'boolean'}
positive_int_schema = {'type': 'integer', 'minimum': 0}
list_of_strings_schema = {'type': 'array', 'items': string_schema}
list_of_positive_int_schema = {'type': 'array', 'items': positive_int_schema}


def handler_schema(schema):
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(request):
            try:
                params = await request.json()
            except json.JSONDecodeError as e:
                return api_response('Invalid json: {}'.format(e), status=False)
            err_list = check_schema(params, schema, name=handler.__name__)
            if err_list:
                return api_response(err_list, status=False)
            return await handler(request)
        return wrapped
    return wrapper


def check_schema(data, schema, err_logs=True, name=''):
    errors = Draft4Validator(schema).iter_errors(data)
    err_list = []
    for err in errors:
        if err.context:
            err_list.extend([
                'root' + ''.join('[{}]'.format(repr(item)) for item in sub_error.path) + ' - ' + sub_error.message
                for sub_error in err.context
            ])
        else:
            path = ''
            if err.path:
                path = 'root' + ''.join('[{}]'.format(repr(item)) for item in err.path) + ' - '
            err_list.append(''.join((path, err.message)))
    if err_list and err_logs:
        logging.error('Failed to validate {} json schema:\n'.format(name) + '\n'.join(err_list))
    return err_list
