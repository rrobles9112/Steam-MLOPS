#!/bin/bash

# Start Jupyter notebook in the background
# jupyter notebook --ip='*' --port=8888 --no-browser --allow-root &

# Start FastAPI app
uvicorn web_server.main:app --host 0.0.0.0 --port 80 --timeout-keep-alive=300