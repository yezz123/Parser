help:
	@echo "Targets:"
	@echo "    make test"
	@echo "    make lint"
	@echo "    make install"

test:
	cd tests && python3 -m unittest discover

lint:
	pre-commit run --all-files

install:
	pip install -r requirements.txt