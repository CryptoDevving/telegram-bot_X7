# DUNE

import os
from datetime import datetime
from requests import get, post


API_KEY = os.getenv("DUNE_API_KEY")
HEADER = {"x-dune-api-key": API_KEY}
BASE_URL = "https://api.dune.com/api/v1/"

VOLUME_TEXT = ""
VOLUME_FLAG = False
VOLUME_TIMESTAMP = datetime.utcnow().timestamp()
VOLUME_LAST_DATE = datetime.fromtimestamp(VOLUME_TIMESTAMP).strftime("%Y-%m-%d %H:%M:%S")

TRENDING_TEXT = ""
TRENDING_FLAG = False
TRENDING_TIMESTAMP = datetime.utcnow().timestamp()
TRENDING_LAST_DATE = datetime.fromtimestamp(TRENDING_TIMESTAMP).strftime("%Y-%m-%d %H:%M:%S")


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