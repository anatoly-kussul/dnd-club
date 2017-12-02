import uuid

import bson
from pymongo.errors import DuplicateKeyError

from dnd_club.helpers import hash_pass, api_response


async def hello_world(request):
    user = request.user
    return api_response(True, 'Hello {}!'.format(user['username']))


async def login(request):
    app = request.app
    params = await request.post()
    username = params.get('username')
    password = params.get('password')
    db = app['db']
    user = await db.users.find_one({'username': username, 'password': hash_pass(password)})
    if not user:
        return api_response(False, 'Wrong username or password')
    token = str(uuid.uuid4())
    app['session_storage'][token] = user
    response = api_response(True, token)
    response.set_cookie('token', token)
    return response


async def logout(request):
    app = request.app
    token = request.cookies.get('token')
    app['session_storage'].pop(token, None)
    response = api_response(True)
    response.set_cookie('token', None)
    return response


async def register(request):
    app = request.app
    db = app['db']
    params = await request.post()
    username = params.get('username')
    password = params.get('password')
    email = params.get('email')
    user = {
        'username': username,
        'password': hash_pass(password),
        'email': email,
    }
    try:
        await db.users.insert_one(user)  # TODO: validate data
        return api_response(True)
    except DuplicateKeyError as e:
        if username in repr(e):
            return api_response(False, 'Username already taken')
        elif email in repr(e):
            return api_response(False, 'This email is already in use')
        else:
            return api_response(False, '{!r}'.format(e))


async def get_class_spells(request):
    app = request.app
    db = app['db']
    params = request.GET
    _class = params.get('class', '')
    spells = await db['{}_spells'.format(_class)].find().to_list(None)
    for spell in spells:
        spell['_id'] = str(spell['_id'])
    return api_response(True, spells)


async def add_favorite(request):
    app = request.app
    db = app['db']
    params = await request.post()
    str_id = params.get('id')
    _class = params.get('class')
    _id = bson.ObjectId(str_id)
    user = request.user
    if _id not in user.get('{}_favorite_spells'.format(_class), []):
        user.setdefault('{}_favorite_spells'.format(_class), []).append(_id)
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'{}_favorite_spells'.format(_class): user['{}_favorite_spells'.format(_class)]}},
    )
    return api_response(True, str_id)


async def remove_favorite(request):
    app = request.app
    db = app['db']
    params = await request.post()
    str_id = params.get('id')
    _class = params.get('class')
    _id = bson.ObjectId(str_id)
    user = request.user
    if _id in user.get('{}_favorite_spells'.format(_class), []):
        user['{}_favorite_spells'.format(_class)].remove(_id)
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'{}_favorite_spells'.format(_class): user['{}_favorite_spells'.format(_class)]}},
    )
    return api_response(True, str_id)


async def get_favorites(request):
    app = request.app
    db = app['db']
    user = request.user
    params = await request.post()
    _class = params.get('class')
    fav = await db['{}_spells'.format(_class)].find(
        {'_id': {'$in': [bson.ObjectId(_id) for _id in user.get('{}_favorite_spells'.format(_class), [])]}}
    ).to_list(None)
    for f in fav:
        f['_id'] = str(f['_id'])
    return api_response(True, fav)
