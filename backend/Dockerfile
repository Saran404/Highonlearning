FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ACCEPT_EULA=Y

# Microsoft ODBC Drivers 17 and 18 for SQL Server (Debian 12 / bookworm)
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl gnupg2 ca-certificates unixodbc \
 && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
 && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends msodbcsql17 msodbcsql18 \
 && printf "\nopenssl_conf = openssl_init\n\n[openssl_init]\nssl_conf = ssl_sect\n\n[ssl_sect]\nsystem_default = system_default_sect\n\n[system_default_sect]\nCipherString = DEFAULT@SECLEVEL=0\n" >> /etc/ssl/openssl.cnf \
 && apt-get purge -y gnupg2 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import pyodbc; drivers = pyodbc.drivers(); assert 'ODBC Driver 17 for SQL Server' in drivers and 'ODBC Driver 18 for SQL Server' in drivers, drivers"

COPY app ./app
COPY scripts ./scripts
RUN useradd --create-home appuser && mkdir -p /srv/uploads && chown -R appuser /srv
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"
# A single worker keeps the in-memory WebSocket registry consistent (see core/websocket_manager.py).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
