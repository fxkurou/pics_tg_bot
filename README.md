# Pics tg bot

## Description
Pics tg bot id a Telegram bot built using the Aiogram framework. It provides various functionalities including pagination and payment features.

## Features
- Help command to provide assistance to users.
- Payment processing with callback handling.
- Integration with Redis for state management.
- Pagination for displaying multiple items in a single message.

## Requirements
- Python 3.12
- Redis
- Docker (optional, for containerization)

## Installation

### Using Docker
1. Build and run the Docker containers:
    ```sh
    docker-compose build
    docker-compose up
    ```

### Without Docker
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Install dependencies:
    ```sh
    pip install poetry
    poetry install
    ```

3. Set up environment variables in a `.env` file. You can use the `.env.template` file as an example.

## Usage
1. Run the bot:
    ```sh
    poetry run python main.py
    ```

## Project Structure
- `bot/`: Contains the bot handlers, states, and utilities.
- `data/`: Contains static files like images.
- `database/`: Contains database models and requests.
- `docker-compose.yaml`: Docker Compose configuration.
- `Dockerfile`: Docker configuration for the bot.
- `pyproject.toml`: Project dependencies and configuration.
- `main.py`: Main entry point for the bot.

## License
This project is licensed under the MIT License.
