# ozi-dashboard

This project provides an ETL pipeline and a PostgreSQL database to store and analyze AS (Autonomous System) statistics. It also includes an optional Redash service for data visualization.

## Prerequisites

- Docker Engine
- Docker Compose

## Setup

1.  **Environment Variables:**

    Create a `.env` file in the root of the project. This file will store the credentials for the PostgreSQL database and any other sensitive configuration. Add the following content to it, replacing the placeholder values with your desired credentials:

    ```env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_OZI_USER=ozi
    POSTGRES_OZI_PASSWORD=strong-password
    REDASH_COOKIE_SECRET=secret
    REDASH_SECRET_KEY=secret
    ```

2.  **Build and Run:**

    To build the images and start the services, run the following command from the project root:

    ```sh
    docker compose up -d
    ```

    This will start the `postgres` and `etl` services.

3.  **Running Redash (Optional):**

    To run the Redash services, use the `redash` profile:

    ```sh
    docker compose --profile redash up -d
    ```

    Once the Redash services are running, you need to create the database tables:

    ```sh
    docker compose run --rm redash-server create_db
    ```

## Accessing Services

-   **PostgreSQL:** The PostgreSQL database will be accessible on `localhost:5432`.
-   **ETL Service:** The ETL service will start and connect to the PostgreSQL database. Check its logs to see its activity:
    ```sh
    docker compose logs -f etl
    ```
-   **Redash:** Redash will be accessible at `http://localhost:5000`.

## Running a Specific ETL Job

The ETL service can be used to run specific jobs by passing command-line arguments to the `etl` service. The available tasks are `ASNS`, `STATS_1D`, `STATS_5M`, `ASN_NEIGHBOURS`, `TRAFFIC`, and `INTERNET_QUALITY`.

Here is an example of how to run the `ASN_NEIGHBOURS` task for the Czech Republic for May 2025:

```sh
docker compose run etl -t ASN_NEIGHBOURS -c CZ -df 2025-05-01 -dt 2025-05-31 -dr D
```

## Stopping Services

To stop the services, run:

```sh
docker compose down
```

To stop the Redash services as well, run:

```sh
docker compose --profile redash down
```

If you want to remove the volumes (including PostgreSQL data), use:

```sh
docker compose down -v
```