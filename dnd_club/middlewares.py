import logging

from aiohttp import web

from dnd_club.helpers import api_response

ALLOWED_HEADERS = ','.join((
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-requested-with',
    'x-csrftoken',
))


def set_cors_headers(request, response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Methods'] = request.method
    response.headers['Access-Control-Allow-Headers'] = ALLOWED_HEADERS
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


async def cors_factory(app, handler):
    async def cors_handler(request):
        # preflight requests
        if request.method == 'OPTIONS':
            return set_cors_headers(request, api_response(True))
        else:
            response = await handler(request)
            return set_cors_headers(request, response)

    return cors_handler


async def suppress_exceptions(app, handler):
    async def middleware(request):
        try:
            return await handler(request)
        except web.HTTPClientError as e:
            return api_response(e.reason, status=False, code=e.status_code)
        except Exception as e:
            logging.critical('Uncaught exception {!r} in \'{}\' handler'.format(e, handler.__name__), exc_info=True)
            return api_response('Internal server error', status=False, code=500)

    return middleware


async def auth(app, handler):
    async def middleware(request):
        def login_required(path):
            result = True
            for r in ['/login', '/register']:
                if path.startswith(r):
                    result = False
            return result

        if login_required(request.path):
            token = request.cookies.get('token')
            if token not in app['session_storage']:
                raise web.HTTPForbidden(reason='Not logged in')
            request.user = app['session_storage'][token]
        return await handler(request)

    return middleware
