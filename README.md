# search-engine
News service Search Engine microservice

![Search Engine Service](https://github.com/DeejayRevok/search-engine/workflows/Search%20Engine%20Service/badge.svg?branch=develop)
[![codecov](https://codecov.io/gh/DeejayRevok/search-engine/branch/develop/graph/badge.svg?token=38GI3NI2MW)](https://codecov.io/gh/DeejayRevok/search-engine)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DeejayRevok_search-engine&metric=alert_status)](https://sonarcloud.io/dashboard?id=DeejayRevok_search-engine)

#### Local running

Run the parent's repo dev docker compose.

Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python webapp/main.py -p LOCAL
```
