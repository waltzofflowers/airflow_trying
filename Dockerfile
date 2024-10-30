# Start from an official Airflow image
FROM apache/airflow:2.10.2

# Install system dependencies and ODBC Driver for SQL Server
USER root
# Update and install required packages
RUN apt-get update && \
    apt-get update && apt-get install -y nano && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remove existing keyring file if it exists and fetch Microsoft key
RUN rm -f /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --batch --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg

# Add Microsoft package repository and install ODBC drivers
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    msodbcsql17 \
    unixodbc \
    unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    # Switch back to airflow user
USER airflow

# Install any Python dependencies (Airflow, pyodbc, SQLAlchemy, etc.)
RUN pip install --no-cache-dir pyodbc sqlalchemy apache-airflow-providers-amazon
# Copy your DAGs folder into the Airflow image
COPY ./dags /opt/airflow/dags
