install:
	poetry install

test:
	poetry run pytest -vv

test-coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m --include=warehouse_manager/* --omit=warehouse_manager/settings.py
	poetry run coverage xml --include=warehouse_manager/* --omit=warehouse_manager/settings.py

dev:
	poetry run uvicorn warehouse_manager.app:app --reload

lint:
	poetry run flake8 warehouse_manager