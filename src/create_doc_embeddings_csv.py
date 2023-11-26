#!/usr/bin/env python

import json
import os
import spacy
from time import sleep
from tqdm import tqdm

import pandas as pd
from sklearn.manifold import TSNE


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS_CSV = os.path.join(ROOT_DIR, "data/filtered_data/filtered_metadata.csv")
VECTOR_JSON = os.path.join(ROOT_DIR, "data/filtered_data/book_vectors.json")
SAMPLE_JSON = os.path.join(ROOT_DIR, "data/filtered_data/sample_vectors.json")


def load_book_csv(doc: str):
    document = pd.read_csv(doc)
    return document


def create_books_path(id: str) -> str:
    book = f"{id}_text.txt"
    book_path = os.path.join(ROOT_DIR, "data/filtered_data/data/text", book)
    return book_path


def handle_year_of_birth(year: float):
    try:
        return int(year)
    except ValueError:
        return "UNKNOWN"


def tsne_cos(book_vectors_df: pd.DataFrame) -> pd.DataFrame:
    """Reduce book vectors from 300-dim to
    2-dim."""
    tsne = TSNE(
        n_components=2,
        verbose=1,
        perplexity=5,  # change to 50 for larger datasets
        n_iter=1000,
        learning_rate=200,
    )
    tsne_vectors = tsne.fit_transform(book_vectors_df)
    tsne_vectors = pd.DataFrame(index=book_vectors_df.index, data=tsne_vectors)
    test = {
        "x_coord": tsne_vectors[0].values,
        "y_coord": tsne_vectors[1].values,
    }
    tsne_vectors = pd.DataFrame(test, index=pd.Index(book_vectors_df.index))
    return tsne_vectors


def get_genre(subject: pd.Series) -> str:
    # Create a genre based on heirarchy of
    # genre categories:
    # fiction
    # adventure
    # fantasy
    # humor
    # horror
    # western
    # science fiction
    # short stories
    if "Science fiction" in subject:
        return "Science Fiction"
    if "Fantasy" in subject:
        return "Fantasy Fiction"
    if "Juvenile fiction" in subject:
        return "Young Adult Fiction"
    if "Mystery fiction" in subject:
        return "Mystery Fiction"
    if "Historical fiction" in subject:
        return "Historical Fiction"
    if "Humor" in subject:
        return "Humor"
    if "Western" in subject:
        return "Western Fiction"
    if "Adventure" in subject:
        return "Adventure Fiction"
    if "Short stories" in subject:
        return "Short Stories"
    return "General Fiction"


def main():
    nlp = spacy.load("en_core_web_lg")
    nlp.max_length = 2000000
    books_metadata_csv = pd.read_csv(BOOKS_CSV)
    books_metadata_csv = books_metadata_csv.reset_index().head(10)
    books_metadata_csv["genre"] = books_metadata_csv["subjects"].apply(
        lambda x: get_genre(x)
    )
    book_vectors = dict()
    book_vector_metadata = []
    # Vectorize books to create metadata json.
    for _, row in tqdm(
        books_metadata_csv.iterrows(),
        total=books_metadata_csv.shape[0],
        desc=f"Vectorizing Books",
    ):
        id = row["id"]
        title = row["title"]
        author = row["author"]
        birth_year = handle_year_of_birth(row["authoryearofbirth"])
        book_path = create_books_path(id)
        genre = row["genre"]
        try:
            try:
                with open(book_path, "r", encoding="utf_8") as src:
                    # TODO: long term we're going to need to
                    # clean these texts
                    book = src.read()
                    doc = nlp(book)
                    # TODO: USE BETTER VECTROIZATION IN FUTURE!
                    book_vector = doc.vector
                    book_vector_metadata.append(
                        {
                            "id": id,
                            "book_path": book_path,
                            "title": title,
                            "vector": book_vector.tolist(),
                            "author": author,
                            "birth_year": birth_year,
                            "genre": genre,
                        }
                    )
                    book_vectors.update(
                        {
                            f"{title}": book_vector,
                        }
                    )
            except FileNotFoundError:
                print(f"file not found: {book_path}")
        except ValueError:
            print(f"file exceeded length 2000000: {book_path}")
    # Convert and write JSON object to file.
    books_df = pd.DataFrame.from_dict(book_vectors, orient="index")
    # Use TSNE to reduce the doc vec embeddings.
    reduced_vectors_df = tsne_cos(books_df)
    reduced_vectors_df.reset_index(inplace=True)
    reduced_vectors_df = reduced_vectors_df.rename(columns={"index": "title"})
    # Merge reduced vectors into data dictionaries.
    for i, book_obj in enumerate(
        tqdm(book_vector_metadata, desc=f"Creating Books JSON")
    ):
        title = book_obj["title"]
        x_coord = reduced_vectors_df[reduced_vectors_df["title"] == title][
            "x_coord"
        ].values[0]
        y_coord = reduced_vectors_df[reduced_vectors_df["title"] == title][
            "y_coord"
        ].values[0]
        book_vector_metadata[i]["x_coord"] = str(x_coord)
        book_vector_metadata[i]["y_coord"] = str(y_coord)
    # Write to JSON
    with open(SAMPLE_JSON, "w", encoding="utf-8") as outfile:
        json.dump(book_vector_metadata, outfile, indent=4)


if __name__ == "__main__":
    main()
