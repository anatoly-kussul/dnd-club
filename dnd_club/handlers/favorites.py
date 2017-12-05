import bson

from dnd_club.errors import ResponseError
from dnd_club.handlers.helpers import get_filtered_spells
from dnd_club.helpers import login_required, api_response
from dnd_club.json_schemas.handlers.favorites import add_favorite_schema, remove_favorite_schema, get_favorites_schema
from dnd_club.json_schemas.helpers import handler_schema


@login_required
@handler_schema(add_favorite_schema)
async def add_favorite(request):
    db = request.app['db']
    user = request.user
    params = await request.json()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    favorites = user['favorites']
    if _id not in favorites:
        favorites.append(_id)
    else:
        raise ResponseError('Already in favorites')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'favorites': favorites}},
    )
    return api_response(str_id)


@login_required
@handler_schema(remove_favorite_schema)
async def remove_favorite(request):
    db = request.app['db']
    user = request.user
    params = await request.json()

    str_id = params.get('id')
    _id = bson.ObjectId(str_id)
    favorites = user['favorites']
    if _id in favorites:
        favorites.remove(_id)
    else:
        raise ResponseError('Not in favorites')
    await db.users.find_one_and_update(
        {'_id': user['_id']},
        {'$set': {'favorites': favorites}},
    )
    return api_response(str_id)


@login_required
@handler_schema(get_favorites_schema)
async def get_favorites(request):
    db = request.app['db']
    user = request.user
    params = await request.json()

    result = await get_filtered_spells(db.spells, params, {'_id': {'$in': user['favorites']}})

    return api_response(result)
