install:
	poetry install

test:
	poetry run pytest -vv

dev:
	poetry run uvicorn warehouse_manager.main:app --reload

lint:
	poetry run flake8 app