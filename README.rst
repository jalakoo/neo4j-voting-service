
Workshop voting service app for introducting graphs to attendees

## Requirements
[Poetry](https://python-poetry.org)

## Installing dependencies
Not necessary if pyproject.toml available
`poetry add streamlit`
`poetry add neo4j`

## Running
`poetry install`
`poetry run python neo4j_voting_service/app.py`

## Tests
`poetry run pytest`

## Troubleshooting
ERROR:
`ERROR tests/test_neo4j_voting_service.py - TypeError: required field "lineno" missing from alias`
SOLUTION:
Update pytest version by removing pytest entry from pyproject.toml then running `poetry add pytest`

ERROR:
`Hint: make sure your test modules/packages have valid Python names.`
SOLUTION:
