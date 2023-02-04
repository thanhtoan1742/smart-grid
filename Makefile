run:
	python3 src/main.py

edit-cpn-export:
	python3 src/edit_cpn_export_function.py

format:
	black .
	isort .

install-dependencies:
	pip install -r src/python-requirements.txt

runcpp:
	g++ cpp/self_gen.cpp -o cpp/self_gen.exe
	./cpp/self_gen