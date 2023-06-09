#!/bin/sh
# python3 initDatabase.py
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v --ignore=fe/data
coverage combine
coverage report
coverage html
