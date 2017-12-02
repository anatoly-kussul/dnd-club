from dnd_club.handlers import (
    hello_world,
    login,
    register,
    logout,
    get_class_spells,
)

routes = [
    ('GET', '/hello_world', hello_world, 'hello_world'),
    ('POST', '/login', login, 'login'),
    ('POST', '/register', register, 'register'),
    ('POST', '/logout', logout, 'logout'),
    ('GET', '/spells', get_class_spells, 'get_class_spells'),
]
