#!/usr/bin/env python
"""Filter Project Gutenberg Metadata CSV to only contain
languages and genres of interest."""

import argparse
import ast
import math
import os
import shutil
import yaml

import pandas as pd
import numpy as np

from typing import List, Dict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _filter_csv_genre(df: pd.DataFrame, genres: List):
    # Lambda function to check if any value in the list is in the dictionary values
    check_value = lambda d: any(val.lower() in d for val in genres)
    # Apply the lambda function and subset the DataFrame
    df2 = df[df["subjects"].apply(check_value)]
    return df2


def _filter_csv_language(df: pd.DataFrame):
    df2 = df = df[df["language"] == "['en']"]
    return df2


def _filter_various_artists(df: pd.DataFrame, authors: List):
    check_value = lambda x: x not in authors
    # Apply the lambda function and subset the DataFrame
    df2 = df[df["author"] != ""]
    df3 = df2[df2["author"].apply(lambda x: not isinstance(x, float))]
    df5 = df3[df3["author"].apply(check_value)]
    return df5


def clean_csv(df: pd.DataFrame, genres: List, authors: List):
    df = _filter_csv_language(df)
    df = _filter_csv_genre(df, genres)
    df = _filter_various_artists(df, authors)
    return df


def main():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    # Create file paths
    META_DATA_CSV_PATH = os.path.join(ROOT_DIR, config["META_DATA_CSV_PATH"])
    META_DATA_OUTPATH = os.path.join(
        ROOT_DIR,
        config["FILTERED_DATA_DIR"],
        config["FILTERED_META_DATA_CSV_OUTPATH"],
    )
    # Check if filepaths have already been written
    # If not write them.
    if not os.path.exists(META_DATA_OUTPATH):
        df = pd.read_csv(META_DATA_CSV_PATH)
        filtered_csv = clean_csv(
            df, genres=config["GENRES"], authors=config["AUTHORS"]
        )
        filtered_csv.to_csv(META_DATA_OUTPATH)
        print(f"Directory created: {META_DATA_OUTPATH}")
    else:
        print(f"Directory already exists: {META_DATA_OUTPATH}")

    # Write filtered files to appropriate directories
    filtered_df = pd.read_csv(META_DATA_OUTPATH)
    book_ids = filtered_df["id"].tolist()
    for id in book_ids:
        DATA_TEXT_PATH = os.path.join(
            ROOT_DIR, config["PATH_TO_TEXT_DATA_FILES"], id + "_text.txt"
        )
        DATA_COUNT_PATH = os.path.join(
            ROOT_DIR,
            config["PATH_TO_TEXT_TOKEN_COUNT_FILES"],
            id + "_counts.txt",
        )
        DATA_TOKENS_PATH = os.path.join(
            ROOT_DIR, config["PATH_TO_TEXT_TOKEN_FILES"], id + "_tokens.txt"
        )
        FILTER_DATA_TEXT_PATH = os.path.join(
            ROOT_DIR,
            config["PATH_TO_FILTERED_TEXT_DATA_FILES"],
            id + "_text.txt",
        )
        FILTER_DATA_COUNT_PATH = os.path.join(
            ROOT_DIR,
            config["PATH_TO_FILTERED_TEXT_COUNT_FILES"],
            id + "_counts.txt",
        )
        FILTER_DATA_TOKENS_PATH = os.path.join(
            ROOT_DIR,
            config["PATH_TO_FILTERED_TEXT_TOKEN_FILES"],
            id + "_tokens.txt",
        )
        if os.path.exists(DATA_TEXT_PATH):
            if os.path.exists(DATA_COUNT_PATH):
                if os.path.exists(DATA_TOKENS_PATH):
                    shutil.copyfile(DATA_TEXT_PATH, FILTER_DATA_TEXT_PATH)
                    shutil.copyfile(DATA_COUNT_PATH, FILTER_DATA_COUNT_PATH)
                    shutil.copyfile(DATA_TOKENS_PATH, FILTER_DATA_TOKENS_PATH)
        else:
            print(f"Directory does not exist: {DATA_TEXT_PATH}")


if __name__ == "__main__":
    # Open and read the YAML file
    main()
