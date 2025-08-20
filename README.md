
# Prefect ETL - Minimal Setup

This repository contains two example ETL flows built with Prefect and two simple runtime options: run locally with Python or run in Docker containers. This README documents the minimal steps to get Prefect running and to execute the example ETL flows.

---

## Summary of Components

- **`etl/basic_etl/`** — a simple flow that fetches JSON from a public API, processes it, and writes `output.csv`.
- **`etl/mongo_db_data_load_etl/`** — a flow that reads a CSV from MinIO and writes records to MongoDB.
- **`infra/docker-compose.yml`** — a Compose file that starts a Prefect server container (uses a Prefect 3 image in the example).

---

## Requirements

- Docker & docker-compose (recommended for a minimal end-to-end setup)
- Or Python 3.11+ and `pip` if you prefer to run flows locally

---

## High-level Checklist

- [x] Inspect repository ETL scripts and Docker configuration
- [x] Create this README with minimal run instructions

---

## 1. Quick Start — Run Prefect Server (Docker)

This will start a local Prefect server UI on port 4200 (per `infra/docker-compose.yml`). From the repo root:

```bash
cd infra
# Start the Prefect server container in the background
docker-compose up -d

# This will automatically create the infra_default network which is used by the ETL service containers to communicate with each other by being on the same network.

# Confirm the container is running
docker-compose ps
```

Open [http://localhost:4200](http://localhost:4200) to access the Prefect UI.

---

## 2. Run the Basic ETL

### Option A — Run Locally with Python (Quick, Minimal)

```bash
cd etl/basic_etl
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# The flow expects CRON_SCHEDULE environment variable when main.py calls to_deployment()
export CRON_SCHEDULE="0 * * * *"  # example: run every hour

python main.py
```

> **Note:** The script will create a deployment and call `serve(...)` (local behavior depends on your Prefect install). `output.csv` will appear in `etl/basic_etl/output.csv` when the flow runs successfully.

### Option B — Run in Docker

```bash
cd etl/basic_etl

# Build and run the service
docker-compose up --build -d

# This will use the infra_default network which is created by infra/docker-compose.yml file.

# View logs
docker-compose logs -f
```

---

## 3. Run the MinIO → MongoDB ETL

This flow (`etl/mongo_db_data_load_etl`) expects a running MinIO and a MongoDB instance. The repository does not include MinIO/Mongo services, so you can run them locally (example below) or point the flow to existing services.

**Minimal example (run temporary MinIO + Mongo with Docker):**

```bash
# Run Mongo
docker run -d --name local-mongo -p 27017:27017 mongo:6

# Run MinIO
docker run -d --name local-minio -p 9000:9000 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin minio/minio server /data

# Create a bucket and upload a CSV (use the MinIO client or the UI at http://localhost:9000)
```

Set required environment variables for the ETL. Create `etl/mongo_db_data_load_etl/.env` (or export them) with these values as an example:

```ini
# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=my-bucket
CSV_OBJECT_NAME=data.csv

# Mongo
MONGO_URI=mongodb://localhost:27017
MONGO_DB=etl_db
MONGO_COLLECTION=records

# Scheduling (used by main.py when deploying)
CRON_SCHEDULE="0 * * * *"
```

**Run the flow locally:**

```bash
cd etl/mongo_db_data_load_etl
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Ensure the env file is loaded (or export variables manually)
export $(cat .env | xargs)

python main.py
```

Or run in Docker by constructing a docker image or a docker-compose service that supplies the same env vars and attaches to the `infra_default` network so the flow can reach Prefect server if needed.

---

## Environment Variables Reference

- **Basic ETL:** `CRON_SCHEDULE` (required by the `to_deployment` call)
- **MinIO→Mongo ETL:** `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET`, `CSV_OBJECT_NAME`, `MONGO_URI`, `MONGO_DB`, `MONGO_COLLECTION`, `CRON_SCHEDULE`

---

## Troubleshooting and Tips

- If `main.py` raises KeyError for `CRON_SCHEDULE`, export the variable before running or put it in an `.env` file and load it.
- If Docker Compose for `etl/basic_etl` complains about missing network `infra_default`, create it with `docker network create infra_default`.
- Prefect UI port is 4200 according to `infra/docker-compose.yml`. If the Prefect server container fails to start, check logs with `docker-compose logs -f` in the `infra` folder.

---

## Files of Interest

- `etl/basic_etl/main.py` — basic flow: fetch → process → save CSV
- `etl/basic_etl/Dockerfile`, `etl/basic_etl/docker-compose.yml` — how to containerize the basic ETL
- `etl/mongo_db_data_load_etl/data_load_etl.py` — MinIO to MongoDB flow implementation
- `etl/mongo_db_data_load_etl/main.py` — deployment wrapper for the MinIO→MongoDB flow
- `infra/docker-compose.yml` — Prefect server container
