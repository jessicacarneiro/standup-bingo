setup-local-env:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	pip install -r test-requirements.txt

setup-env:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

test:
	pytest tests/

test-verbose:
	pytest tests/ -v

test-file:
	@echo "Usage: make test-file FILE=tests/test_bingo_generator.py"
	@if [ -z "$(FILE)" ]; then \
		echo "Please specify a test file: make test-file FILE=tests/test_bingo_generator.py"; \
	else \
		pytest $(FILE) -v; \
	fi

test-class:
	@echo "Usage: make test-class CLASS=tests.test_bingo_generator.TestBingoGenerator"
	@if [ -z "$(CLASS)" ]; then \
		echo "Please specify a test class: make test-class CLASS=tests.test_bingo_generator.TestBingoGenerator"; \
	else \
		python -m unittest $(CLASS) -v; \
	fi

test-method:
	@echo "Usage: make test-method METHOD=tests.test_bingo_generator.TestBingoGenerator.test_generate_bingo_card_valid_input"
	@if [ -z "$(METHOD)" ]; then \
		echo "Please specify a test method: make test-method METHOD=tests.test_bingo_generator.TestBingoGenerator.test_generate_bingo_card_valid_input"; \
	else \
		python -m unittest $(METHOD) -v; \
	fi

test-coverage:
	pytest tests/ --cov=bingo_generator --cov-report=html --cov-report=term

clean:
	rm *.pdf