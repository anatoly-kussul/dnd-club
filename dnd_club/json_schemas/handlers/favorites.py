from dnd_club.json_schemas.helpers import string_schema

add_favorite_schema = {
    'type': 'object',
    'properties': {
        'id': string_schema,
    },
    'additionalProperties': False,
    'required': ['id'],
}
remove_favorite_schema = {
    'type': 'object',
    'properties': {
        'id': string_schema,
    },
    'additionalProperties': False,
    'required': ['id'],
}
