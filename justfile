python := shell("cat .python-version")

# Print this help documentation
help:
    just --list

# Run linting
lint:
    ruff check src tests

# Run static typechecking
typecheck:
    mypy src --install-types --non-interactive

# Run the tests
test *args:
    uv run --python {{python}} --isolated --no-editable --no-dev --group tests --reinstall \
        python -I -m pytest {{args}}
