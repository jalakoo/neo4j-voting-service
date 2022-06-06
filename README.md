
Workshop voting service app for introducting graphs to attendees

## Requirements
[Poetry](https://python-poetry.org)

## Installing dependencies
Not necessary if pyproject.toml available
`poetry add streamlit`
`poetry add neo4j`

## Running
`poetry install`
`poetry run streamlit run neo4j_voting_service/app.py`

## Tests
`poetry run pytest`

## Database Setup
If needing to recreate source database, run the following cypher commands to set up basic elements.
```
CREATE DATABASE votes
CREATE CONSTRAINT unique_user FOR (user:User) REQUIRE user.name IS UNIQUE
CREATE CONSTRAINT unique_question FOR (question:Question) REQUIRE question.name IS UNIQUE
CREATE CONSTRAINT unique_choice FOR (choice:Choice) REQUIRE choice.name IS UNIQUE
CREATE USER explorer IF NOT EXISTS SET PLAINTEXT PASSWORD “exploring” SET STATUS ACTIVE SET HOME DATABASE votes
```

## Troubleshooting
ERROR:
`ERROR tests/test_neo4j_voting_service.py - TypeError: required field "lineno" missing from alias`
SOLUTION:
Update pytest version by removing pytest entry from pyproject.toml then running `poetry add pytest`

ERROR:
`Hint: make sure your test modules/packages have valid Python names.`
SOLUTION:
