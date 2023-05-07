
start: venv
	# need to fix path to static files
	. venv/bin/activate && uvicorn src.petfinder.api:app --reload

debug: venv
	. venv/bin/activate && pushd src && python -m petfinder.api

requirements.txt:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.

venv: requirements.txt

open:
	open http://127.0.0.1:8000/static/index.html

update: venv
	. venv/bin/activate && . ./.env && python ./src/petfinder/export.py --exclude "English Bulldog" search

.PHONY: start requirements