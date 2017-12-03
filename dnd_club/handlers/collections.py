from dnd_club.errors import ResponseError
from dnd_club.helpers import login_required, api_response


@login_required
async def create_collection(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    collection_name = params.get('name')
    if collection_name not in user['collections']:
        user['collections'][collection_name] = []
    else:
        raise ResponseError('Duplicate collection name')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'collections.{}'.format(collection_name): user['collections'][collection_name]}}
    )
    return api_response(collection_name)


@login_required
async def delete_collection(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    collection_name = params.get('name')
    if collection_name in user['collections']:
        user['collections'].pop(collection_name)
    else:
        raise ResponseError('No such collection')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$unset': {'collections.{}'.format(collection_name): 1}}
    )
    return api_response(collection_name)