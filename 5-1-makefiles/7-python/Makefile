.DEFAULT_GOAL := run

DB := /project/sharespace.db

setup: requirements.txt
	pip install -r requirements.txt

# Build the DB only if it doesn't exist (or if create_db.py is newer)
$(DB): create_db.py
	python3 create_db.py

run: setup $(DB)
	python3 -m flask -A project/app.py run --host=0.0.0.0

test: setup $(DB)
	python3 -m pytest

clean:
	rm -rf __pycache__
	rm -rf project/__pycache__
	rm -f $(DB)

.PHONY: run clean setup test

