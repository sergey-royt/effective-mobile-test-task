install:
	poetry install

test:
	poetry run pytest -vv

dev:
	poetry run uvicorn app.main:app --reload

lint:
	poetry run flake8 app