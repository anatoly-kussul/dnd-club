import hashlib
import logging
import logging.config

from aiohttp.web import json_response, HTTPForbidden


def api_response(data=None, status=True, code=200):
    return json_response(
        {
            'status': status,
            'data': data,
        },
        status=code,
    )


def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(handler):
    async def wrapper(request):
        app = request.app
        token = request.cookies.get('token')
        if token not in app['session_storage']:
            raise HTTPForbidden(reason='Not logged in')
        request.user = app['session_storage'][token]
        return await handler(request)
    return wrapper


def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': ['console'],
            },
            # 'aiohttp': {
            #     'level': 'WARNING',
            # },
        },
    })
