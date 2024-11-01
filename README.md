# Data Orchestration with Airflow

This project demonstrates how to use Apache Airflow to orchestrate data workflows, connecting to an MSSQL database, retrieving data, and shipping it to an S3-compatible storage solution using MinIO.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Workflow Overview](#workflow-overview)
- [License](#license)

## Features

- Connects to an MSSQL database to retrieve data.
- Uses Apache Airflow for workflow orchestration.
- Ships retrieved data to a MinIO S3 bucket.
- Supports easy modification and extension of data workflows.

## Technologies

- [Apache Airflow](https://airflow.apache.org/)
- [MSSQL Database](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- [MinIO](https://min.io/) (S3-compatible object storage)

## Setup

1. **Clone the repository:**

        bash
        git clone https://github.com/yourusername/your-repo.git
        cd your-repo

2. **Install dependencies:**

Make sure you have Python installed, then set up a virtual environment and install the required packages.

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install apache-airflow
    pip install pyodbc  # For MSSQL connection
    pip install minio   # For interacting with MinIO

3. **Configure Airflow: Initialize the Airflow database:**

        airflow db init

Set up your Airflow environment variables as needed.

4. **Configure MSSQL and MinIO:**

Update the Airflow connection settings in the airflow.cfg or via the Airflow UI to include your MSSQL and MinIO connection details.

## Usage

1. **Start Airflow:**

Launch the Airflow web server and scheduler:

        airflow webserver --port 8080
        airflow scheduler

2. **Access the Airflow UI:**

Open your browser and go to http://localhost:8080 to access the Airflow dashboard.

3. **Trigger the DAG:**

From the Airflow UI, you can trigger the DAG to start retrieving data from MSSQL and shipping it to MinIO.

## Workflow Overview

1. **Data Extraction:**

- The DAG connects to the MSSQL database.
- Data is queried and extracted.

2. **Data Loading:**

- Extracted data is formatted as needed.
- Data is uploaded to the MinIO S3 bucket.
