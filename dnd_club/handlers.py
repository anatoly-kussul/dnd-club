import uuid

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
    spells = [spell async for spell in db['{}_spells'.format(_class)].find()]
    for spell in spells:
        spell['_id'] = str(spell['_id'])
    import logging
    logging.critical(spells)
    return api_response(True, spells)
