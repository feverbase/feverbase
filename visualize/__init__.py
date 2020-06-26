import sys
import json
import re
import logging

sys.path.append("../")
from utils import db, ms, config

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

import plotly.express as px

logger = logging.getLogger(__name__)


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

        # convert timestamp to epoch
        if doc.timestamp:
            entry_json["parsed_timestamp"] = int(doc.timestamp.timestamp())
        else:
            entry_json["parsed_timestamp"] = -1

        parsed_documents.append(entry_json)
    logger.warn(f"Visualization retrieved {len(parsed_documents)} documents from MongoDB")
    return parsed_documents


def create_vis(documents):
    timestamps = []
    for doc in documents:
        if doc.get("timestamp"):
            unix = doc["timestamp"]["$date"]
            date = dt.datetime.fromtimestamp(unix/1000.0)
            timestamps.append(date)
    fig = px.histogram(timestamps, nbins=len(documents))
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    fig.show()
    # plt.hist(timestamps, len(documents))
    # plt.subplots_adjust(bottom=0.2)
    # plt.xticks( rotation=25 )
    # ax=plt.gca()
    # xfmt = md.DateFormatter('%Y-%m-%d')
    # ax.xaxis.set_major_formatter(xfmt)
    # plt.show()


def mongo_to_vis():
    # if not on prod, dont push to meili (to prevent accidents)
    if not (config.MONGODB_URI or "").startswith("mongodb+srv://prod:"):
        return

    docs = parse_documents()
    create_vis(docs)

