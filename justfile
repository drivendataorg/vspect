# Keep in sync with just-version in .github/workflows/*.yml
set minimum-version := '1.55.0'

python := shell("cat .python-version")

# Print this help documentation
help:
    just --list

# Run linting
lint:
    ruff check src tests

# Audit GitHub Actions workflows with zizmor (passes through args)
zizmor *args:
    uvx --exclude-newer "7 days" zizmor .github/ {{args}}

# Run static typechecking
typecheck:
    mypy src --install-types --non-interactive

# Run the tests
test *args:
    uv run --python {{python}} --isolated --no-editable --no-dev --group tests --reinstall \
        python -I -m pytest {{args}}

docs:
    griffe2md vspect -o docs/api-reference.md
