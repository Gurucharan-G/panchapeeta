# Troubleshooting Guide - Server Error Resolution

This document summarizes the diagnostics, verification steps, and resolution for the `500 Internal Server Error` affecting the live website.

## Diagnostic Steps

### 1. Database & Environment Verification
We verified that database credentials and S3 credentials in the production `.env` file were valid. Migrations and connection health were confirmed on the RDS PostgreSQL database by running `showmigrations` under the `panchapeethas` system user:
```bash
sudo -u panchapeethas /opt/panchapeethas/app/venv/bin/python /opt/panchapeethas/app/manage.py showmigrations
```

### 2. WSGI Request & View Simulation
We simulated incoming request routing to `/` (the homepage view) using Django's WSGI application handler directly in the Python shell with `DEBUG = True` and `DEBUG = False`:
```bash
sudo -u panchapeethas env $(sudo cat /opt/panchapeethas/app/.env | grep -v '^#' | xargs) /opt/panchapeethas/app/venv/bin/python /opt/panchapeethas/app/manage.py shell -c "
import io
from config.wsgi import application
environ = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/',
    'SERVER_NAME': 'panchapeeta.org',
    'SERVER_PORT': '80',
    'HTTP_HOST': 'panchapeeta.org',
    'HTTP_X_FORWARDED_PROTO': 'https',
    'wsgi.url_scheme': 'https',
    'wsgi.input': io.BytesIO(b''),
}
def start_response(status, headers):
    print('STATUS:', status)
    print('HEADERS:', headers)

for chunk in application(environ, start_response):
    print(chunk[:1000])
"
```
Both test simulations returned `STATUS: 200 OK` successfully. This proved that the Python code, PostgreSQL connection, and S3-based `STORAGES` dictionary were fully functional.

### 3. Service Environment & State Verification
We inspected the active environment variables of the running Gunicorn processes via `/proc/<PID>/environ` and verified that:
- Nginx correctly forwarded SSL headers (`Host`, `X-Forwarded-Proto`).
- The `.env` file used standard Unix line endings (no Windows carriage returns `\r\n`).

## Resolution

Gunicorn was serving a stale instance of the Django application because it had not been restarted since the modern `STORAGES` dictionary settings were updated. 

Restarting the Gunicorn systemd service successfully loaded the new Django storage configuration:
```bash
sudo systemctl restart panchapeethas
```

After the restart, `https://panchapeeta.org` is fully operational and loads successfully with HTTP `200 OK` responses.
