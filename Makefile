run:
	python3 main.py

format:
	black .
	isort .

install-dependencies:
	pip install -r src/python-requirements.txt