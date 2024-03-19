#!/bin/bash

# Start Jupyter notebook in the background
jupyter notebook --ip='*' --port=8888 --no-browser --allow-root &

# Start FastAPI app
uvicorn api.main:app --host 0.0.0.0 --port 5000