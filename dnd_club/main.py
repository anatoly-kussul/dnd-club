import asyncio
import logging

from aiohttp import web
from motor import motor_asyncio
from pymongo.errors import DuplicateKeyError

import settings
from dnd_club.helpers import setup_logging, hash_pass
from dnd_club.routes import routes
from dnd_club.middlewares import suppress_exceptions, auth


async def init_db():
    mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_HOST, settings.MONGO_PORT)
    db = mongo_client[settings.MONGO_DB]
    await db.users.create_index('username', unique=True)
    await db.users.create_index('email', unique=True)
    admin = {
        'username': 'admin',
        'password': hash_pass('admin'),
        'email': 'admin@dnd-club'
    }
    try:
        await db.users.insert_one(admin)
    except DuplicateKeyError:
        pass
    return db


def init_app(loop=None):
    app = web.Application(
        middlewares=[
            suppress_exceptions,
            auth,
        ],
        loop=loop
    )

    app['db'] = loop.run_until_complete(init_db())
    app['session_storage'] = {}

    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    return app


def run_app(app, *, host='0.0.0.0', port=None,
            shutdown_timeout=60.0, ssl_context=None):
    if port is None:
        if not ssl_context:
            port = 8080
        else:
            port = 8443

    loop = app.loop

    handler = app.make_handler()
    srv = loop.run_until_complete(loop.create_server(handler, host, port,
                                                     ssl=ssl_context))

    scheme = 'https' if ssl_context else 'http'
    prompt = '127.0.0.1' if host == '0.0.0.0' else host
    logging.info("Started on {scheme}://{prompt}:{port}/".format(scheme=scheme, prompt=prompt, port=port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no branch
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(handler.finish_connections(shutdown_timeout))
        loop.run_until_complete(app.cleanup())
    loop.close()


def main():
    setup_logging()
    loop = asyncio.get_event_loop()
    app = init_app(loop=loop)
    try:
        run_app(app, port=settings.PORT)
    finally:
        logging.info('Stopped.')


if __name__ == '__main__':
    main()
