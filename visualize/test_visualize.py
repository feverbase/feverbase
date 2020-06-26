import sys
sys.path.append("../")
from visualize import mongo_to_vis

if __name__ == "__main__":
    res = mongo_to_vis()
    print(res)