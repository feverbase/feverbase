import sys
sys.path.append("../")
from utils import ms

from search import perform_meili_search

client = ms.get_ms_client()
index = ms.get_ms_trials_index(client)
