#!/usr/bin/env python

import os
import yaml


def create_directory_if_not_exists(directory_path):
    """
    Creates a new directory at the specified path if it does not already exist.

    Args:
    directory_path (str): The path of the directory to create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")


if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    create_directory_if_not_exists(config["FILTERED_DATA_DIR"])
    create_directory_if_not_exists(config["PATH_TO_FILTERED_TEXT_DATA_FILES"])
    create_directory_if_not_exists(config["PATH_TO_FILTERED_TEXT_TOKEN_FILES"])
    create_directory_if_not_exists(config["PATH_TO_FILTERED_TEXT_COUNT_FILES"])
