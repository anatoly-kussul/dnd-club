from dnd_club.json_schemas.helpers import string_schema

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
