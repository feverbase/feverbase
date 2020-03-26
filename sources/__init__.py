from . import chictr # Chinese Clinical Trial Registry
from . import clinicaltrialsgov # US National Library of Medicine Clinial Trials
from . import eu # EU Clinial Trials Register
from . import isrctn # ISRCTN: primary clinial trial registry recognised by WHO and ICMJE
from . import utils

TERMS = utils.get_query_terms()

def get_records():
    data = []
    for query in TERMS:
        data.extend(chictr.find(query))
        data.extend(clinicaltrialsgov.find(query))
        # data.extend(eu.find(query))
        data.extend(isrctn.find(query))
    # sort the data and return it
    data = sorted(data, key=lambda d: d["timestamp"], reverse=True)
    return data