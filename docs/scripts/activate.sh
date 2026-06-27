#!/bin/bash

source venv/bin/activate

export PYSPARK_PYTHON="$(pwd)/venv/bin/python"
export PYSPARK_DRIVER_PYTHON="$(pwd)/venv/bin/python"

export PATH="/opt/homebrew/bin:$PATH"