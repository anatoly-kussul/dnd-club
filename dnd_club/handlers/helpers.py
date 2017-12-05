import math


def filter_spells(spells_collection, params, additional_filter=None):
    filter_params = {}
    if additional_filter is not None:
        filter_params = additional_filter
    if 'level' in params:
        filter_params['lvl.{}'.format(params['class'])] = {'$in': params['level']}
    else:
        filter_params['lvl.{}'.format(params['class'])] = {'$exists': True}
    if 'name' in params:
        filter_params['name'] = {'$regex': '.*{}.*'.format(params['name']), '$options': 'i'}
    for param in ['school', 'source']:
        if params.get(param):
            filter_params[param] = {'$in': params[param]}
    spells_query = spells_collection.find(filter_params)

    return spells_query


def paginate_spells(spells_query, page, per_page):
    spells_query.skip((page - 1) * per_page).limit(per_page)
    return spells_query


async def get_filtered_spells(spells_collection, params, additional_filter=None):
    filtered_query = filter_spells(spells_collection, params, additional_filter=additional_filter)
    pages = 1
    if 'page' in params:
        pages = math.ceil((await filtered_query.count())/params['per_page'])
        filtered_query = paginate_spells(filtered_query, params['page'], params['per_page'])
    spells_list = await filtered_query.to_list(None)
    return {'spells': spells_list, 'pages': pages}
