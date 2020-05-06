import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get(
    "MONGODB_TEST_URI" if os.environ.get("PYTESTING") else "MONGODB_URI"
)

FILTER_OPTION_KEYS = [
    "sponsor",
    # "location",
    "recruiting_status",
]
