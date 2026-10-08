.PHONY: doctor test lint format eval-fast eval-dev genome-show compile tree aide-status aide-validate aide-dry-run

doctor:
	uv run forge doctor

test:
	uv run pytest

lint:
	uv run ruff check forge tests scripts

format:
	uv run ruff format forge tests scripts

eval-fast:
	uv run forge eval --split regression --limit 25

eval-dev:
	uv run forge eval --split dev

genome-show:
	uv run forge genome show --path config/genome.yaml

compile:
	python -m compileall -q forge tests scripts

tree:
	find . -path './.git' -prune -o -path './.venv' -prune -o -type f -print | sort


aide-status:
	uv run forge aide status

aide-validate:
	uv run forge aide validate

aide-dry-run:
	uv run forge aide dry-run
