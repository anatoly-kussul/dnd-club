from dnd_club.json_schemas.helpers import (
    positive_int_schema,
    list_of_strings_schema,
    string_schema,
    list_of_positive_int_schema,
)

get_spells_schema = {
    'type': 'object',
    'properties': {
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
