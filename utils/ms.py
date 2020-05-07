import os
import meilisearch
import logging

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

def get_ms_client():
    master_key = os.environ.get("MEILI_KEY")
    url = os.environ.get("MEILI_URL")

    if not master_key or not url:
        raise Exception('No Meilisearch master key and/or URL specified.')

    return meilisearch.Client(url, master_key)


def get_ms_trials_index(client):
    client = get_ms_client()
    indexes = client.get_indexes()

    # no indexes, create one
    if indexes == []:
        logger.warn("[Meili] No index 'trials', creating...")
        index = client.create_index(uid="trials", primary_key="ms-id")
    else:
        # if index exists already
        logger.warn("[Meili] Index 'trials' already exists")
        index = client.get_index("trials")

    return index
