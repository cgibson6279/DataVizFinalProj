
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_JSON = os.path.join(ROOT_DIR, "data/filtered_data/book_vectors.json")
CLEAN_VECTOR_JSON = os.path.join(ROOT_DIR, "data/filtered_data/book_vectors_clean.json")
SAMPLE_JSON = os.path.join(ROOT_DIR, "data/filtered_data/sample_vectors.json")
SAMPLE2_JSON = os.path.join(ROOT_DIR, "data/filtered_data/sample_vectors2.json")
CLEAN_VECTORS_JSON_2 = os.path.join(ROOT_DIR, "data/filtered_data/book_vectors_no_vector.json")

if __name__ == "__main__":
    with open(CLEAN_VECTOR_JSON, "r", encoding="utf-8") as src:
        samples = json.load(src)
    for sample in samples:
        sample["x_coord"] = float(sample["x_coord"])
        sample["y_coord"] = float(sample["y_coord"])
        del sample["vector"]
    # Write to JSON
    with open(CLEAN_VECTORS_JSON_2, "w", encoding="utf-8") as outfile:
        json.dump(samples, outfile, indent=4)

