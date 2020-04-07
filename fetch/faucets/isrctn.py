import xml.etree.ElementTree as ET
import requests
import utils
import logging
import json
import os
from pprint import pprint

SOURCE = "isrctn.com"
FILENAME = "isrctn.json"
API_URL = "http://www.isrctn.com/api/query/format/who?q={query}"
LOG_FILENAME = "logs/isrctn.log"



def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def find(query):
    data = {}
    count = 0
    url = API_URL.format(query=query)
    results = requests.get(url).text

    root = ET.fromstring(results)

    for trial in root.iter("trial"):
        this_entry = {"_source": SOURCE}
        main = trial.find("main")
        trial_id = main.find("trial_id").text
        date_registration = main.find("date_registration").text
        title = main.find("public_title").text
        sponsor = main.find("primary_sponsor").text
        sample_size = int(main.find("target_size").text)
        url = main.find("url").text
        recruitment_status = main.find("recruitment_status").text
        sex = trial.find("criteria").find("gender").text

        if main.find("hc_freetext") != None:
            target_disease = main.find("hc_freetext").text
        else:
            target_disease = None

        if main.find("i_freetext") != None:
            summary = main.find("i_freetext").text
        else:
            summary = None

        contacts = trial.find("contacts")
        contacts_list = contacts.findall("contact")
        # 0th is always blank for some reason
        if len(contacts_list) >= 2:
            primary_contact = contacts_list[1]
            first_name = primary_contact.find("firstname").text
            last_name = primary_contact.find("lastname").text
            phone = primary_contact.find("telephone").text
            email = primary_contact.find("email").text
            city = primary_contact.find("city").text
            country = primary_contact.find("country1").text

            this_entry["contact"] = {
                    "name": f"{first_name} {last_name}",
                    "phone": phone,
                    "email": email,
                }


        this_entry["title"] = title
        this_entry["url"] = url
        this_entry["timestamp"] = date_registration
        this_entry["sponsor"] = sponsor
        this_entry["sample_size"] = sample_size
        this_entry["recruiting_status"] = recruitment_status
        this_entry["sex"] = sex
        this_entry["target_disease"] = target_disease
        this_entry["summary"] = summary

        pprint(this_entry)

        data[url] = this_entry
        count += 1
        logging.info(f"Parsed {url}")


    print(f"Fetched {count} results for {query}")
    return data


