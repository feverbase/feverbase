import json
import os

FOLDER = os.path.abspath(os.path.dirname(__file__))

def get_query_terms():
    queries = []
    with open(os.path.join(FOLDER, "queries.txt")) as f:
        queries = f.read().splitlines()
    return queries

def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in list(d.items()):
        if not value:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience