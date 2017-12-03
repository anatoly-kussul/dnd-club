from dnd_club.helpers import api_response


async def get_class_spells(request):
    db = request.app['db']
    params = request.GET

    _class = params.get('class', '')
    spells = await db.spells.find({'lvl.{}'.format(_class): {'$exists': True}}).to_list(None)
    return api_response(spells)
