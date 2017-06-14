from aiohttp.web import json_response

async def hello_world(request):
    data = {
        'status': True,
        'data': 'Hello World!'
    }
    return json_response(data)
