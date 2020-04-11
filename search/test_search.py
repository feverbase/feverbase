import sys
sys.path.append("../")
from search import perform_meili_search

if __name__ == "__main__":
    query = sys.argv[1]
    res = perform_meili_search(query).get("hits")
    if res:
        print(len(res))
    else:
        print("No results")
