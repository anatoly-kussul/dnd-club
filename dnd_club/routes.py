from dnd_club.handlers import (
    hello_world,
    login,
    register,
    logout,
)

routes = [
    ('GET', '/hello_world', hello_world, 'hello_world'),
    ('POST', '/login', login, 'login'),
    ('POST', '/register', register, 'register'),
    ('POST', '/logout', logout, 'logout'),
]
