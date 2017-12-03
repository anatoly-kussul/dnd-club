import bson

from dnd_club.errors import ResponseError
from dnd_club.helpers import login_required, api_response


@login_required
async def add_favorite(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    favorites = user['collections']['favorites']
    if _id not in favorites:
        favorites.append(_id)
    else:
        raise ResponseError('Already in favorites')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'collections.favorites': favorites}},
    )
    return api_response(str_id)


@login_required
async def remove_favorite(request):
    db = request.app['db']
    user = request.user
    params = await request.post()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    favorites = user['collections']['favorites']
    if _id in favorites:
        favorites.remove(_id)
    else:
        raise ResponseError('Not in favorites')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'collections.favorites': favorites}},
    )
    return api_response(str_id)


@login_required
async def get_favorites(request):
    db = request.app['db']
    user = request.user

    fav = await db.spells.find(
        {'_id': {'$in': [bson.ObjectId(_id) for _id in user['collections']['favorites']]}}
    ).to_list(None)
    return api_response(fav)
