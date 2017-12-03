from aiohttp.web import HTTPClientError


class ResponseError(HTTPClientError):
    status_code = 200

    def __init__(self, reason):
        super().__init__(reason=reason)
