# hackathon-llm

Backend and API endpoints for Q-Summit Hackathon Challenge.

### Installation

Create your virtual environment using:

```bash
virtualenv -p 3.10 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install the pre-commit hook:

```bash
pre-commit install
```

### Setup

Create a .env file with following content. Note: some variables might not be required for your use case. Add them as you go.

```bash
OPENAI_API_KEY=

PAPERS_CORE_API=
PAPERS_SEMANTIC_SCHOLAR=
```

### Run files

Start your python scripts from the root directory directly using a command like this:

```bash
python -m src.api.some_cool_file
```

Note that there dots are used as delimiters and there is no .py extension at the end.


### Compress files

```
zip -r database/vector_db.zip database/vector_db
unzip database/vector_db.zip -d database/vector_db

```
