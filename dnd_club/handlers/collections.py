import bson

from dnd_club.errors import ResponseError
from dnd_club.helpers import login_required, api_response


@login_required
async def create_collection(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    collection_name = params.get('collection_name')
    if collection_name in user['collections']:
        raise ResponseError('Duplicate collection name')
    user['collections'][collection_name] = []
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

    collection_name = params.get('collection_name')
    if collection_name not in user['collections']:
        raise ResponseError('No such collection')
    user['collections'].pop(collection_name)
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$unset': {'collections.{}'.format(collection_name): 1}}
    )
    return api_response(collection_name)


@login_required
async def add_to_collection(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    collection_name = params.get('collection_name')

    if collection_name not in user['collections']:
        raise ResponseError('No such collection')
    collection = user['collections'][collection_name]
    if _id in collection:
        raise ResponseError('Already in collection')
    collection.append(_id)

    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'collections.{}'.format(collection_name): collection}},
    )
    return api_response(str_id)


@login_required
async def remove_from_collection(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    collection_name = params.get('collection_name')

    if collection_name not in user['collections']:
        raise ResponseError('No such collection')
    collection = user['collections'][collection_name]
    if _id not in collection:
        raise ResponseError('Not in collection')
    collection.remove(_id)

    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'collections.{}'.format(collection_name): collection}},
    )
    return api_response(str_id)


@login_required
async def get_collection(request):
    db = request.app['db']
    user = request.user
    params = request.GET

    collection_name = params.get('collection_name')
    if collection_name not in user['collections']:
        raise ResponseError('No such collection')
    spells = await db.spells.find(
        {'_id': {'$in': user['collections'][collection_name]}}
    ).to_list(None)
    return api_response(spells)
