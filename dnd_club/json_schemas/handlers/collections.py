from dnd_club.json_schemas.helpers import (
    string_schema,
    list_of_strings_schema,
    list_of_positive_int_schema,
    positive_int_schema,
)

create_collection_schema = {
    'type': 'object',
    'properties': {
        'collection_name': string_schema,
    },
    'additionalProperties': False,
    'required': ['collection_name'],
}
delete_collection_schema = {
    'type': 'object',
    'properties': {
        'collection_name': string_schema,
    },
    'additionalProperties': False,
    'required': ['collection_name'],
}
add_to_collection_schema = {
    'type': 'object',
    'properties': {
        'collection_name': string_schema,
        'id': string_schema,
    },
    'additionalProperties': False,
    'required': ['collection_name', 'id'],
}
remove_from_collection_schema = {
    'type': 'object',
    'properties': {
        'collection_name': string_schema,
        'id': string_schema,
    },
    'additionalProperties': False,
    'required': ['collection_name', 'id'],
}
get_collection_schema = {
    'type': 'object',
    'properties': {
        'collection_name': string_schema,
        'class': string_schema,
        'name': string_schema,
        'school': list_of_strings_schema,
        'source': list_of_strings_schema,
        'level': list_of_positive_int_schema,
        'page': positive_int_schema,
        'per_page': positive_int_schema,
    },
    'additionalProperties': False,
    'required': ['collection_name', 'class'],
    'dependencies': {
        'page': ['per_page'],
        'per_page': ['page'],
    },
}
