from dnd_club.handlers.helpers import get_filtered_spells
from dnd_club.helpers import api_response
from dnd_club.json_schemas.handlers.spells import get_spells_schema
from dnd_club.json_schemas.helpers import handler_schema


@handler_schema(get_spells_schema)
async def get_spells(request):
    db = request.app['db']
    params = await request.json()

    result = await get_filtered_spells(db.spells, params)

    return api_response(result)
