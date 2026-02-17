#!/usr/bin/env python3

import os
from pathlib import Path

DB_PATH = Path("./project/sharespace.db")

def main():
    # Ensure parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create the file if it doesn't exist
    if not DB_PATH.exists():
        with DB_PATH.open("w") as f:
            f.write("This is a dummy database file.\n")
        print(f"Created {DB_PATH}")
    else:
        print(f"{DB_PATH} already exists.")

if __name__ == "__main__":
    main()

