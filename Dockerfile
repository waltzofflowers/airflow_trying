# Start from an official Airflow image
FROM apache/airflow:2.10.2

# Install system dependencies and ODBC Driver for SQL Server
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends nano curl gnupg2 && \
    apt-get install -y python3-pip && \
    pip install --upgrade pip && \
    pip install --upgrade apache-airflow-providers-amazon && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fetch Microsoft key and install ODBC drivers
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --batch --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" | tee /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends msodbcsql17 unixodbc unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies
RUN pip install --no-cache-dir pyodbc sqlalchemy apache-airflow-providers-amazon==2.3.0

# Copy your DAGs folder into the Airflow image
COPY ./dags /opt/airflow/dags
