from dnd_club import constants

email_schema = {
    'type': 'string',
    'pattern': constants.EMAIL_REGEX,
}
username_schema = {
    'type': 'string',
    'pattern': constants.USERNAME_REGEX,
}
password_schema = {
    'type': 'string',
    'pattern': constants.PASSWORD_REGEX,
}

# HANDLERS SCHEMAS
login_schema = {
    'type': 'object',
    'properties': {
        'email': email_schema,
        'password': password_schema,
    },
    'required': ['email', 'password'],
    'additionalProperties': False,
}
register_schema = {
    'type': 'object',
    'properties': {
        'email': email_schema,
        'password': password_schema,
        'username': username_schema,
    },
    'required': ['email', 'password', 'username'],
    'additionalProperties': False,
}
change_pass_schema = {
    'type': 'object',
    'properties': {
        'old_password': password_schema,
        'new_password': password_schema,
    },
    'required': ['old_password', 'new_password'],
    'additionalProperties': False,
}
