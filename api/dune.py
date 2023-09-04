import os
import random

import requests

BASE_URL = "https://api.dune.com/api/v1/"

API_KEYS = (
    os.getenv("DUNE_API_KEY"),
    os.getenv("DUNE_API_KEY_2"),
    os.getenv("DUNE_API_KEY_3"),
    os.getenv("DUNE_API_KEY_4")
)


def get_random_header() -> dict:
    return {"x-dune-api-key": random.choice(API_KEYS)}


def make_api_url(module: str, action: str, identifier: str) -> str:
    return f"{BASE_URL}{module}/{identifier}/{action}"


def execute_query(query_id: str, engine: str = "small") -> str:
    response = requests.post(
        make_api_url("query", "execute", query_id),
        headers=get_random_header(),
        params={"performance": engine}
    )
    return response.json()["execution_id"]


def get_query_status(execution_id: str) -> requests.Response:
    return requests.get(make_api_url("execution", "status", execution_id), headers=get_random_header())


def get_query_results(execution_id: str) -> requests.Response:
    return requests.get(make_api_url("execution", "results", execution_id), headers=get_random_header())


def cancel_query_execution(execution_id: str) -> requests.Response:
    return requests.get(make_api_url("execution", "cancel", execution_id), headers=get_random_header())
