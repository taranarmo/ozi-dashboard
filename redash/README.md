# Redash Deployment

This repository contains the necessary files to deploy Redash using Docker Compose.

## Prerequisites

- Docker installed
- Docker Compose installed

## Setup

1.  **Clone this repository:**
    ```bash
    git clone <your-repo-url>
    cd hetzner
    ```

2.  **Configure environment variables:**
    Open the `.env` file and replace the placeholder values with strong, random strings:
    - `POSTGRES_PASSWORD`
    - `REDASH_COOKIE_SECRET`
    - `REDASH_SECRET_KEY`

3.  **Run the setup script:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

## Access Redash

Once the services are running, you can access Redash at `http://localhost:5000`. The initial setup will prompt you to create an admin user.

## Stopping Redash

To stop Redash services, run:
```bash
docker-compose down
```
