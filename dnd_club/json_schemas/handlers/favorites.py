from dnd_club.json_schemas.helpers import (
    string_schema,
    list_of_strings_schema,
    list_of_positive_int_schema,
    positive_int_schema,
)

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
get_favorites_schema = {
    'type': 'object',
    'properties': {
        # 'collection_name': string_schema,
        'class': string_schema,
        'name': string_schema,
        'school': list_of_strings_schema,
        'source': list_of_strings_schema,
        'level': list_of_positive_int_schema,
        'page': positive_int_schema,
        'per_page': positive_int_schema,
    },
    'additionalProperties': False,
    'required': ['class'],
    'dependencies': {
        'page': ['per_page'],
        'per_page': ['page'],
    },
}
