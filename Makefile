install:
	uv sync

run:
	python3 fly-in.py config.txt

debug:
	python3 -m pdb fly-in.py

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache

.PHONY: install run debug clean lint