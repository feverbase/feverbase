import sys
from . import chictr  # Chinese Clinical Trial Registry
from . import clinicaltrialsgov  # US National Library of Medicine Clinial Trials
from . import eu  # EU Clinical Trials Register
from . import (
    isrctn,
)  # ISRCTN: primary clinial trial registry recognised by WHO and ICMJE
from . import utils

sys.path.append('../')
from utils import db

TERMS = utils.get_query_terms()

########################################################
### UPDATE TRANSLATE FUNCTION WHEN ADDING NEW SOURCE ###
########################################################


def get_records():
    data = {}
    for query in TERMS:
        try:
            print(f"Crawling {chictr.SOURCE}...")
            data.update(chictr.find(query))
        except Exception as e:
            print(e)

        try:
            print(f"Crawling {clinicaltrialsgov.SOURCE}...")
            data.update(clinicaltrialsgov.find(query))
        except Exception as e:
            print(e)

        try:
            print(f"Crawling {eu.SOURCE}...")
            data.update(eu.find(query))
        except Exception as e:
            print(e)

        try:
            print(f"Crawling {isrctn.SOURCE}...")
            data.update(isrctn.find(query))
        except Exception as e:
            print(e)

    articles = [translate(i) for i in data.values()]
    
    db.create(articles)

    return articles


def translate(info):
    source = info["SOURCE"]
    if source == chictr.SOURCE:
        return chictr.translate(info)
    elif source == clinicaltrialsgov.SOURCE:
        return clinicaltrialsgov.translate(info)
    elif source == eu.SOURCE:
        return eu.translate(info)
    elif source == isrctn.SOURCE:
        return isrctn.translate(info)
    return info
