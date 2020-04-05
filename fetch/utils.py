import json
import os

FOLDER = os.path.abspath(os.path.dirname(__file__))

def get_query_terms():
    queries = []
    with open(os.path.join(FOLDER, "queries.txt")) as f:
        queries = f.read().splitlines()
    return queries