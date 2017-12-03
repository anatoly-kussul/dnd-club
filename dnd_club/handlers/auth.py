import uuid

from pymongo.errors import DuplicateKeyError

from dnd_club.errors import ResponseError
from dnd_club.helpers import hash_pass, api_response, login_required


async def login(request):
    app = request.app
    db = app['db']

    params = await request.post()
    email = params.get('email')
    password = params.get('password')
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


async def register(request):
    db = request.app['db']
    params = await request.post()

    username = params.get('username')
    password = params.get('password')
    email = params.get('email')
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
