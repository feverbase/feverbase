from bs4 import BeautifulSoup
import requests
import utils
from pprint import pprint

FILENAME = "isrctn.json"
BASE_URL = "https://www.isrctn.com"
QUERY_URL = "{BASE_URL}/search?q={query}"
PAGINATE_QUERY = "&page={page_num}&searchType=basic-search"


def to_iso8601(date):
    comps = date.split("/")
    return f"{comps[2]}-{comps[1]}-{comps[0]}"


def parse_plain_english_summary(summary):
    p1 = "Background and study aims"
    p2 = "Who can participate?"
    p3 = "What does the study involve?"
    p4 = "What are the possible benefits and risks of participating?"
    p5 = "Where is the study run from?"
    p6 = "When is the study starting and how long is it expected to run for?"
    p7 = "Who is funding the study?"
    p8 = "Who is the main contact?"
    background_study_aims = summary.split(p1)[1].split(p2)[0]
    who_can_participate = summary.split(p2)[1].split(p3)[0]
    study_involves = summary.split(p3)[1].split(p4)[0]
    benefits_risks = summary.split(p4)[1].split(p5)[0]
    where_run_from = summary.split(p5)[1].split(p6)[0]
    when_start_how_long = summary.split(p6)[1].split(p7)[0]
    who_funding = summary.split(p7)[1].split(p8)[0]
    main_contact = summary.split(p8)[1]

    summary_data = {
        "background_study_aims": background_study_aims,
        "who_can_participate": who_can_participate,
        "study_involves": study_involves,
        "benefits_risks": benefits_risks,
        "where_run_from": where_run_from,
        "when_start_how_long": when_start_how_long,
        "who_funding": who_funding,
        "main_contact": main_contact,
    }

    # pprint(summary_data)
    return summary_data


def find(query):
    data = {}
    count = 0
    url = QUERY_URL.format(BASE_URL=BASE_URL, query=query)
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")

        results_number = soup.findAll("span", {"class": "Control_name"})
        if len(results_number) == 0:
            num_pages = 0
        else:
            num_pages = int(results_number[1].text.split("of")[1].strip())

        for page_num in range(num_pages):
            url = QUERY_URL.format(
                BASE_URL=BASE_URL, query=query
            ) + PAGINATE_QUERY.format(page_num=page_num)
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                my_lis = soup.findAll("li", {"class": "ResultsList_item"})
                for result in my_lis:
                    for link in result.find_all("a", href=True):
                        isrctn_id = link.text.split(":")[0].strip()
                        title = link.text.split(":")[1].strip()
                        link = link.get("href").split("?")[0]
                        if link:
                            url = f"{BASE_URL}{link}"
                            page = requests.get(url)
                            if page.status_code == 200:
                                soup = BeautifulSoup(page.content, "html.parser")
                                dds = soup.findAll("dd", {"class": "Meta_value"})
                                dd_texts = [dd.text.strip() for dd in dds]

                                condition_category = dd_texts[0]
                                date_applied = to_iso8601(dd_texts[1])
                                date_assigned = to_iso8601(dd_texts[2])
                                last_edited = to_iso8601(dd_texts[3])
                                prospective_retrospective = dd_texts[4]
                                overall_trial_status = dd_texts[5]
                                recruitment_status = dd_texts[6]

                                ps = soup.findAll("p")
                                plain_english_summary = ps[0].text
                                summary_data = parse_plain_english_summary(
                                    plain_english_summary
                                )
                                cleaned_ps = [p.text.strip().rstrip() for p in ps[1:]]
                                # TODO: Get all additional data
                                # example url: https://www.isrctn.com/ISRCTN51287266?q=covid&filters=&sort=&offset=4&totalResults=4&page=1&pageSize=10&searchType=basic-search

                                data[url] = {
                                    "id": isrctn_id,
                                    "url": url,
                                    "timestamp": last_edited,
                                    "title": title,
                                    "condition_category": condition_category,
                                    "date_applied": date_applied,
                                    "date_assigned": date_assigned,
                                    "last_edited": last_edited,
                                    "prospective_retrospective": prospective_retrospective,
                                    "overall_trial_status": overall_trial_status,
                                    "recruitment_status": recruitment_status,
                                    "summary": summary_data,
                                }
                                count += 1

    print(f"Fetched {count} results for {query}")
    return data
