# ozi-dashboard

1. Create Postgres instance on GCP, name it `asn-stats`
2. Use strong password for user `postgres` while creating DB
3. Go to `asn-stats`'s console
4. Download code by cloning Git Repository

    ```
    git clone https://github.com/lab4-berlin/ozi-dashboard
    ```

5. Create database, user and tables for asn_stats project

    - when asked for password use postgres password from step 2 first
    - and asn_data password for the second sql script

    ```
    cd ozi-dashboard
    ./init_database.sh
    ```

## TMP

```
cat sql/*.sql | gcloud sql connect asn-stats2 --user=asn_stats
```

## Dagster

```
sudo apt install python3-pip
sudo apt install python3.12-venv
python3 -m venv dagster_env
source dagster_env/bin/activate
pip install dagster dagster-webserver dagster-postgres
dagster project scaffold --name=dagster_etl
```

## Dockerization

This application can be built and run as a Docker container.

### Prerequisites

*   Docker installed on your system.
*   A running PostgreSQL database accessible to the container.
*   The database schema should be initialized (e.g., by running the SQL scripts like `create_database_schema.sql` and `insert_countries.sql` against your target database).

### Building the Image

To build the Docker image, navigate to the root directory of the project (where the `Dockerfile` is located) and run:

```sh
docker build -t as-stats-etl .
```

### Running the Container

To run the Docker container, you need to provide several environment variables for database configuration and specify the path to the job YAML file you want to execute.

**Environment Variables:**

*   `OZI_DATABASE_USER`: The username for the database.
*   `OZI_DATABASE_PASSWORD`: The password for the database user.
*   `OZI_DATABASE_NAME`: The name of the database.
*   `OZI_DATABASE_HOST`: The hostname or IP address of the database server.
*   `OZI_DATABASE_PORT`: The port number for the database server (default for PostgreSQL is 5432).

**Command-line Argument:**

*   You must append the path to the specific job YAML file (located within the `etl/jobs/` directory in the container) to the `docker run` command.

**Example `docker run` command:**

```sh
docker run --rm \
  -e OZI_DATABASE_USER=your_db_user \
  -e OZI_DATABASE_PASSWORD=your_db_password \
  -e OZI_DATABASE_NAME=your_db_name \
  -e OZI_DATABASE_HOST=your_db_host \
  -e OZI_DATABASE_PORT=5432 \
  as-stats-etl etl/jobs/load_asns_report_May25.yaml
```

Replace `your_db_user`, `your_db_password`, `your_db_name`, and `your_db_host` with your actual database credentials and host. The `--rm` flag automatically removes the container when it exits.
