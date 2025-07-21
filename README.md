# ozi-dashboard

This project provides an ETL pipeline and a PostgreSQL database to store and analyze AS (Autonomous System) statistics. It also includes an optional Redash service for data visualization.

## Prerequisites

- Docker Engine
- Docker Compose

## Setup

1.  **Environment Variables:**

    Create two environment files in the root of the project: `.env.ozi` and `.env.redash`.

    **`.env.ozi`**

    This file stores the credentials for the OZI PostgreSQL database. Create the file and add the following content, replacing the placeholder values with your desired credentials:

    ```env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_OZI_USER=ozi
    POSTGRES_OZI_PASSWORD=strong-password
    ```

    **`.env.redash`**

    This file stores the credentials for the Redash services. Create the file and add the following content:

    ```env
    REDASH_COOKIE_SECRET=placeholder
    REDASH_SECRET_KEY=placeholder
    REDASH_POSTGRES_PASSWORD=placeholder
    ```

    To generate strong random values for `REDASH_COOKIE_SECRET`, `REDASH_SECRET_KEY`, and `REDASH_POSTGRES_PASSWORD`, you can use the following command:

    ```sh
    # For REDASH_COOKIE_SECRET and REDASH_SECRET_KEY
    openssl rand -hex 32

    # For REDASH_POSTGRES_PASSWORD
    openssl rand -hex 16
    ```

    Copy the generated values into the `.env.redash` file.

2.  **Build and Run:**

    To build the images and start the services, run the following command from the project root:

    ```sh
    docker compose up -d
    ```

    This will start the `ozi-postgres` and `ozi-etl` services.

3.  **Running Redash (Optional):**

    To run the Redash services, you first need to create the database tables. Run the following command:

    ```sh
    docker compose run --rm redash-server create_db
    ```

    Then, to start the Redash services, use the `redash` profile:

    ```sh
    docker compose --profile redash up -d
    ```

## Accessing Services

Services are accessible in two ways:

-   **From your local machine (the host):** Services with published ports can be accessed via `localhost`.
    -   **OZI PostgreSQL:** `localhost:5432`
    -   **Redash:** `http://localhost:5000`
-   **From other services within Docker:** Services connect to each other using their service names as hostnames. For example, the `ozi-etl` service connects to the database at `ozi-postgres:5432`.

You can monitor the ETL service logs with:
```sh
docker compose logs -f ozi-etl
```

## Running a Specific ETL Job

The ETL service can be used to run specific jobs by passing command-line arguments to the `etl` service. The available tasks are `ASNS`, `STATS_1D`, `STATS_5M`, `ASN_NEIGHBOURS`, `TRAFFIC`, and `INTERNET_QUALITY`.

Here is an example of how to run the `ASN_NEIGHBOURS` task for the Czech Republic for May 2025:

```sh
docker compose run ozi-etl -t ASN_NEIGHBOURS -c CZ -df 2025-05-01 -dt 2025-05-31 -dr D
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
