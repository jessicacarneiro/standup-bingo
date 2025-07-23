setup-local-env:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	pip install -r test-requirements.txt

setup-env:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

clean:
	rm *.pdf