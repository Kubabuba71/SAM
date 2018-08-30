import logging
from datetime import datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


def logged(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        # log.debug(res)
        print(f'DEBUG-{now}: {res}')
        return res
    return decorated
