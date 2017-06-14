from dnd_club.handlers import hello_world

routes = [
    ('GET', '/hello_world', hello_world, 'hello_world'),
]
