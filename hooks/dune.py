# DUNE

import os
from datetime import datetime
from requests import get, post


API_KEY = os.getenv("DUNE_API_KEY")
HEADER = {"x-dune-api-key": API_KEY}
BASE_URL = "https://api.dune.com/api/v1/"

FLAG = False
TIMESTAMP = datetime.utcnow().timestamp()
LAST_DATE = datetime.fromtimestamp(TIMESTAMP).strftime("%Y-%m-%d %H:%M:%S")
VOLUME = ""
TRENDING = ""


def make_api_url(module, action, identifier):
    return f"{BASE_URL}{module}/{identifier}/{action}"


def execute_query(query_id, engine="small"):
    response = post(
        make_api_url("query", "execute", query_id),
        headers=HEADER,
        params={"performance": engine},
    )
    return response.json()["execution_id"]


def get_query_status(execution_id):
    return get(make_api_url("execution", "status", execution_id), headers=HEADER)


def get_query_results(execution_id):
    return get(make_api_url("execution", "results", execution_id), headers=HEADER)


def cancel_query_execution(execution_id):
    return get(make_api_url("execution", "cancel", execution_id), headers=HEADER)