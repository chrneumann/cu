import os
import os.path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_customers(paths):
    """Load customer data from given YAML file paths.

    Paths may be absolute or working directory relative.
    """
    customers = []
    for path in paths:
        path = os.path.join(os.getcwd(), path)
        with file(path, 'r') as stream:
            data = load(stream, Loader=Loader)
            data['filename'] = os.path.splitext(os.path.basename(path))[0]
        customers.append(data)
    return customers
