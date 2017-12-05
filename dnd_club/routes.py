from dnd_club.handlers import *

routes = [
    # auth
    ('POST', '/login', login, 'login'),
    ('POST', '/register', register, 'register'),
    ('POST', '/logout', logout, 'logout'),
    ('POST', '/change_pass', change_password, 'change_pass'),
    ('GET', '/get_user_data', get_user_data, 'get_user_data'),

    # spells
    ('POST', '/spells', get_spells, 'get_class_spells'),

    # favorites
    ('POST', '/add_fav', add_favorite, 'add_fav'),
    ('POST', '/get_fav', get_favorites, 'get_fav'),
    ('POST', '/rem_fav', remove_favorite, 'rem_fav'),

    # collections
    ('POST', '/create_collection', create_collection, 'create_collection'),
    ('POST', '/delete_collection', delete_collection, 'delete_collection'),
    ('POST', '/add_to_collection', add_to_collection, 'add_to_collection'),
    ('POST', '/remove_from_collection', remove_from_collection, 'remove_from_collection'),
    ('POST', '/get_collection', get_collection, 'get_collection'),
]
