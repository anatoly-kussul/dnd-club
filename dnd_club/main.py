import asyncio
import logging

from aiohttp import web
from motor import motor_asyncio
from pymongo.errors import DuplicateKeyError

import settings
from dnd_club.helpers import setup_logging, hash_pass
from dnd_club.routes import routes
from dnd_club.middlewares import suppress_exceptions, cors_factory


async def init_db():
    mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_HOST, settings.MONGO_PORT)

    # await mongo_client.drop_database(settings.MONGO_DB)

    db = mongo_client[settings.MONGO_DB]
    await db.users.create_index('email', unique=True)
    await db.spells.create_index('name', unique=True)

    # import json
    # spells = {}
    # for _class in ['wizard', 'cleric']:
    #     with open('{}.json'.format(_class)) as f:
    #         data = json.load(f)
    #         for spell in data:
    #             spell['description'] = eval(spell['description']).decode().strip()
    #             spell['lvl'] = {_class: int(spell['lvl'])}
    #             spell['school'] = list(spell['school'].split('/'))
    #             saved_spell = spells.setdefault(spell['name'], spell)
    #             saved_spell['lvl'].update(spell['lvl'])
    # await db.spells.insert_many(spells.values())

    admin = {
        'username': 'admin',
        'password': hash_pass('admin'),
        'email': 'admin@dnd-club',
        'collections': {},
        'favorites': [],
    }
    try:
        await db.users.insert_one(admin)
    except DuplicateKeyError:
        pass
    return db


def init_app(loop=None):
    app = web.Application(
        middlewares=[
            cors_factory,
            suppress_exceptions,
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
