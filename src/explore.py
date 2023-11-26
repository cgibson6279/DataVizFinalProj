import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_VECTOR_JSON = os.path.join(ROOT_DIR, "data/filtered_data/book_vectors_clean.json")

if __name__ == "__main__":
    with open(CLEAN_VECTOR_JSON, "r", encoding="utf-8") as src:
        samples = json.load(src)
    genres = set()
    authors = set()

    for sample in samples:
        if type(sample["x_coord"]) != float or type(sample["y_coord"] != float): 
            print(type(sample["x_coord"]), "\t" ,type(sample["y_coord"]))
            # genres.add(sample["genre"])
