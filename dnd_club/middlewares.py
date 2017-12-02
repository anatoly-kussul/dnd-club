import logging

from aiohttp import web

from dnd_club.helpers import api_response


async def suppress_exceptions(app, handler):
    async def middleware(request):
        try:
            return await handler(request)
        except web.HTTPClientError as e:
            return api_response(False, e.reason, code=e.status_code)
        except Exception as e:
            logging.critical('Uncaught exception {!r} in \'{}\' handler'.format(e, handler.__name__), exc_info=True)
            return api_response(False, 'Internal server error', code=500)

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
