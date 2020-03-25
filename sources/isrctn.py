from bs4 import BeautifulSoup
import requests
import utils

FILENAME = "isrctn.json"
BASE_URL = "https://www.isrctn.com"
QUERY_URL = "{BASE_URL}/search?q={query}"
PAGINATE_QUERY = "&page={page_num}&searchType=basic-search"

TERMS = utils.get_query_terms()

data = []

for query in TERMS:
    count = 0
    url = QUERY_URL.format(BASE_URL=BASE_URL, query=query)
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        results_number = soup.findAll("span", {"class": "Control_name"})
        if len(results_number) == 0:
            num_pages = 0
        else:
            num_pages = int(results_number[1].text.split("of")[1].strip())

        for page_num in range(num_pages):
            url = QUERY_URL.format(BASE_URL=BASE_URL, query=query) + PAGINATE_QUERY.format(page_num=page_num)
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                my_lis = soup.findAll("li", {"class": "ResultsList_item"})
                for result in my_lis:
                    for link in result.find_all('a', href=True):
                        link = link.get("href")
                        if link:
                            data.append({"link": f"{BASE_URL}{link}"})
                            count += 1
    print(f"Fetched {count} results for {query}")

utils.save_json(data, FILENAME)
