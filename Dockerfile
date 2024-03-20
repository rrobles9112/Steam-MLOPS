# Use the light version of Python 3.11
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /api

# Copy the current directory contents into the container at /app
COPY . /api

# Install poetry
RUN pip install poetry

# Install dependencies using poetry
RUN poetry config virtualenvs.create false \
  && poetry install

# Make port 80 available to the world outside this container
EXPOSE 80

# Run FastAPI app on port 5000
# Run Jupyter notebook server when the container launches
# Give execution rights to the entrypoint script
RUN chmod +x /api/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/api/entrypoint.sh"]

