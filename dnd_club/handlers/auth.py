import uuid

from pymongo.errors import DuplicateKeyError

from dnd_club.errors import ResponseError
from dnd_club.helpers import hash_pass, api_response, login_required
from dnd_club.json_schemas.handlers.auth import login_schema, register_schema, change_pass_schema
from dnd_club.json_schemas.helpers import handler_schema


@handler_schema(login_schema)
async def login(request):
    app = request.app
    db = app['db']

    params = await request.json()
    email = params['email']
    password = params['password']
    user = await db.users.find_one({'email': email, 'password': hash_pass(password)})
    if not user:
        raise ResponseError('Wrong username or password')
    token = str(uuid.uuid4())
    app['session_storage'][token] = user
    response = api_response(token)
    response.set_cookie('token', token)
    return response


@login_required
async def logout(request):
    app = request.app

    token = request.cookies.get('token')
    app['session_storage'].pop(token, None)
    response = api_response(True)
    response.del_cookie('token')
    return response


@handler_schema(register_schema)
async def register(request):
    db = request.app['db']
    params = await request.json()

    username = params['username']
    password = params['password']
    email = params['email']
    user = {
        'username': username,
        'password': hash_pass(password),
        'email': email,
        'collections': {},
        'favorites': [],
    }
    try:
        await db.users.insert_one(user)  # TODO: validate data
        return api_response(True)
    except DuplicateKeyError as e:
        if username in repr(e):
            raise ResponseError('Username already taken')
        elif email in repr(e):
            raise ResponseError('This email is already in use')
        else:
            raise


@login_required
async def get_user_data(request):
    user = request.user
    user_dict = {
        'username': user['username'],
        'email': user['email'],
        'collections': list(user['collections'].keys()),
    }
    return api_response(user_dict)


@login_required
@handler_schema(change_pass_schema)
async def change_password(request):
    db = request.app['db']
    user = request.user
    params = await request.json()

    old_password = params['old_password']
    new_password = params['new_password']

    if hash_pass(old_password) != user['password']:
        raise ResponseError('Wrong password')

    user['password'] = hash_pass(new_password)
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'password': user['password']}}
    )

    return api_response(True)
