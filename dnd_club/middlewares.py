import logging

from aiohttp import web

async def suppress_exceptions(app, handler):
    async def middleware(request):
        try:
            return await handler(request)
        except web.HTTPClientError as e:
            data = {
                'status': False,
                'data': e.reason,
            }
            return web.json_response(data, status=e.status_code)
        except Exception as e:
            logging.critical('Uncaught exception {!r} in \'{}\' handler'.format(e, handler.__name__), exc_info=True)
            data = {
                'status': False,
                'data': 'Internal server error.'
            }
            return web.json_response(data, status=500)

    return middleware
