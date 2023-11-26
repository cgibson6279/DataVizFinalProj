#!/bin/bash
"""
Create data directory if needed.
"""
set -euxo pipefail

main() {
    chmod +x src/create_data_dir.py
    chmod +x src/preprocess.py

    ./src/create_data_dir.py
    ./src/preprocess.py
}

main 