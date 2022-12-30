test:
	poetry run pytest
format:
	poetry run black tests bsharp
run:
	poetry run python -m bsharp
doc:
	poetry run pdoc -o docs bsharp

.PHONY: test format bsharp doc
