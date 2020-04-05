import sys
# from faucets import (
#     chictr,
#     clinicaltrialsgov,
#     eu,
#     isrctn
# ) 
sys.path.append('./fetch')
from faucets import clinicaltrialsgov
from . import utils

sys.path.append('../')
from utils import db

TERMS = utils.get_query_terms()

########################################################
### UPDATE TRANSLATE FUNCTION WHEN ADDING NEW SOURCE ###
########################################################

def get_records():
    data = {}
    for query in TERMS[4:5]:
        # try:
        #     print(f"Crawling {chictr.SOURCE}...")
        #     data.update(chictr.find(query))
        # except Exception as e:
        #     print(e)
        
        # import pdb; pdb.set_trace()

        try:
            print(f"Crawling {clinicaltrialsgov.SOURCE}...")
            data.update(clinicaltrialsgov.find(query))
        except Exception as e:
            print(e)

        # import pdb; pdb.set_trace()

        # try:
        #     print(f"Crawling {eu.SOURCE}...")
        #     data.update(eu.find(query))
        # except Exception as e:
        #     print(e)

        # import pdb; pdb.set_trace()

        # try:
        #     print(f"Crawling {isrctn.SOURCE}...")
        #     data.update(isrctn.find(query))
        # except Exception as e:
        #     print(e)

        # import pdb; pdb.set_trace()

    articles = [translate(i) for i in data.values()]
    
    db.create(articles)

    return articles


def translate(info):
    source = info["SOURCE"]
    # if source == chictr.SOURCE:
    #     return chictr.translate(info)
    if source == clinicaltrialsgov.SOURCE:
        return utils.del_none(clinicaltrialsgov.translate(info))
    # elif source == eu.SOURCE:
    #     return eu.translate(info)
    # elif source == isrctn.SOURCE:
    #     return isrctn.translate(info)
    return info
