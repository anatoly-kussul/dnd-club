from dnd_club.handlers import (
    hello_world,
    login,
    register,
    logout,
    get_class_spells,
    add_favorite,
    get_favorites,
    remove_favorite,
    get_user_data,
    create_collection,
    delete_collection,
)

routes = [
    ('GET', '/hello_world', hello_world, 'hello_world'),
    ('POST', '/login', login, 'login'),
    ('POST', '/register', register, 'register'),
    ('POST', '/logout', logout, 'logout'),
    ('GET', '/spells', get_class_spells, 'get_class_spells'),
    ('POST', '/add_fav', add_favorite, 'add_fav'),
    ('GET', '/get_fav', get_favorites, 'get_fav'),
    ('POST', '/rem_fav', remove_favorite, 'rem_fav'),
    ('GET', '/get_user_data', get_user_data, 'get_user_data'),
    ('POST', '/create_collection', create_collection, 'create_collection'),
    ('POST', '/delete_collection', delete_collection, 'delete_collection'),
]
