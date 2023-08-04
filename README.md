# Geospatial queries with LLMs

This repository contains code, queries and prompts for a prototype
system that can interact with geospatial data based on a user's query.


## Running
Install the necessary requirements:
```
pip install -r requirements.txt
```

Run a standalone query with prompt using `query.py`:
```
python query.py -p prompts/v6.txt -q "$(cat queries/q2.txt)" -m gpt-4 -t 0
```

Run the mult-step prompt with `query_steps.py`:
```
python query_steps.py -p prompts/steps/v1/ -m gpt-4
```

Run the arbitrary data search using `data_search.py`:
```
python data_search.py -p prompts/steps/v1
```
