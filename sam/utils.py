import logging

log = logging.getLogger(__name__)


def logged(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        log.debug(res)
        return res
    return decorated
