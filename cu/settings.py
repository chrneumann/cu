import os.path
import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_local_settings():
    """Traverse current path up to the next configuration and return it.
    """
    config = _find_local_configuration(os.getcwd())
    data = None
    if config is not None:
        stream = open(config, 'r')
        data = load(stream, Loader=Loader)
    return data


def _find_local_configuration(path):
    current = os.path.normpath(path)
    config = None
    while not config:
        config = os.path.join(current, '.cu.yml')
        if not os.path.isfile(config):
            config = None
        if os.path.dirname(current) == current:
            break
        current = os.path.dirname(current)
    return config
