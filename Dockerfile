# Use the light version of Python 3.11
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry
RUN pip install poetry

# Install dependencies using poetry
RUN poetry config virtualenvs.create false \
  && poetry install

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Jupyter notebook when the container launches
CMD ["jupyter", "notebook", "--ip='*'", "--port=80", "--no-browser", "--allow-root"]
