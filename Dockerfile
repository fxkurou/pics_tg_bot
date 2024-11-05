FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app

# Copy project files into the container
COPY pyproject.toml /usr/src/app/

# Install Poetry
RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

# Copy the project code into the container
COPY . .