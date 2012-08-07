import os.path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_customers(basedir, files):
    """Load customer data from given paths.
    """
    customers = []
    for path in files:
        path = os.path.join(basedir, path)
        with open(path, 'r') as stream:
            data = load(stream, Loader=Loader)
            data['filename'] = os.path.splitext(os.path.basename(path))[0]
        customers.append(data)
    return customers
