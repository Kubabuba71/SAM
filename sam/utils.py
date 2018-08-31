from datetime import datetime

log = print


def logged(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        # log.debug(res)
        print(f'DEBUG-{now}: RES: {res}')
        return res
    return decorated


def parse_action(action: str):
    action_components = action.split('.')
    if len(action_components) == 1:
        return action_components[0], None, None

    elif len(action_components) == 2:
        return action_components[0], action_components[1],  None

    elif len(action_components) == 3:
        return action_components[0], action_components[1], action_components[2]


def normalize_volume_value(volume):
    if isinstance(volume, str):
        volume = int(volume.strip().replace('%', ''))
    return volume
