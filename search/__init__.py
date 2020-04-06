import sys
sys.path.append('../')
from utils import db, ms
import json

def parse_documents():
    parsed_documents = []
    for doc in db.Article.objects:
        entry_json = json.loads(doc.to_json())

        # these values should be guaranteed by Mongo
        _id = entry_json.get("_id")
        assert _id, "_id not present in Mongo document"
        oid = _id.get("$oid")
        assert oid, "$oid not present in Mongo document"

        # remove _id key so we can feed directly to meili
        del entry_json["_id"]
        entry_json["ms-id"] = oid

        parsed_documents.append(entry_json)
    print(f"Retrieved {len(parsed_documents)} documents from MongoDB")
    return parsed_documents

def push_to_meili(documents):
    client = ms.get_ms_client()
    index = ms.get_ms_trials_index(client)
    update_id = index.add_documents(documents).get("updateId")

    # don't return until all documents have been pushed
    status = None
    while status != "processed":
       update_status = index.get_update_status(update_id)
       status = update_status.get("status")
    print("Successfully uploaded data to Meilisearch")

def mongo_to_meili():
    docs = parse_documents()
    push_to_meili(docs)

def perform_meili_search(query):
    client = ms.get_ms_client()
    index = ms.get_ms_trials_index(client)
    result = index.search(query)
    print(result)