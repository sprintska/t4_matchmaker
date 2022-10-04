"""Flask configuration."""

import os

TESTING = os.environ("MATCHMAKER_TESTING") if "MATCHMAKER_TESTING" in os.environ else 0
DEBUG = os.environ("MATCHMAKER_DEBUG") if "MATCHMAKER_DEBUG" in os.environ else 0
SECRET_KEY = (
    os.environ("MATCHMAKER_SECRET_KEY")
    if "MATCHMAKER_SECRET_KEY" in os.os.environ
    else 0
)
HASURA_AUTH_KEY = (
    os.environ("MATCHMAKER_HASURA_AUTH_KEY")
    if "MATCHMAKER_HASURA_AUTH_KEY" in os.environ
    else 0
)
HASURA_API_URL = (
    os.environ("MATCHMAKER_HASURA_API_URL")
    if "MATCHMAKER_HASURA_API_URL" in os.environ
    else "localhost:8080"
)
