import os.path
import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_local_settings():
    """Traverse current path up to the next configuration.

    Returns a tuple (path, settings) where path is the path of the
    configuration and settings is a hash containing the parsed
    settings.
    """
    config = _find_local_configuration(os.getcwd())
    data = None
    if config is not None:
        with open(config, 'r') as stream:
            data = load(stream, Loader=Loader)
    return (config, data)


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
