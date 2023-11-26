#!/usr/bin/env python

import spacy
import os
import json
import pandas as pd


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS_CSV = os.join(ROOT_DIR, "data/filtered_data/filtered_metadata.csv")


def vectorize_doc():
    pass


def main():
    books_csv = pd.read_csv(ROOT_DIR)


if __name__ == "__main__":
    main()
