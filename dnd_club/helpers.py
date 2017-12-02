import hashlib
import logging
import sys

from aiohttp.web import json_response


def api_response(status, data=None, code=200):
    return json_response(
        {
            'status': status,
            'data': data,
        },
        status=code,
    )


def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def setup_logging(verbose=True, silent=False):
    fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
    if verbose:
        logging_level = logging.DEBUG
    elif silent:
        logging_level = logging.CRITICAL
    else:
        logging_level = logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level, format=fmt)
    if not verbose:
        logging.getLogger('aiohttp').setLevel(logging.WARNING)
