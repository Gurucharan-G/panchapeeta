# 🐍 Deploying the Panchapeetas Django App on PythonAnywhere

This guide walks you through deploying your **Veerashaiva Pancha Peethas** Django application on PythonAnywhere, configuring it with your GoDaddy custom domain.

---

## Prerequisites
1. A **PythonAnywhere Account** (For custom domains, you need a paid plan starting at $5/mo).
2. A **GoDaddy Domain** (e.g., `panchapeethas.org`).

---

## Step 1 — Clone Code & Create Virtual Environment

1. Log in to **PythonAnywhere**.
2. Open a **Bash Console** from your dashboard.
3. Clone your GitHub repository:
   ```bash
   git clone https://github.com/Gurucharan-G/panchapeeta.git
   cd panchapeeta
   ```

4. Create a virtual environment using Python 3.10 (or matching version):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Step 2 — Create the Environment File (`.env`)

1. Inside the console, create the `.env` file:
   ```bash
   nano .env
   ```
2. Paste the following configuration (replace placeholders with your real credentials):
   ```ini
   DJANGO_SECRET_KEY=your-secret-key-here
   PRODUCTION=True
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,yourusername.pythonanywhere.com
   ```
   *(Press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit).*

---

## Step 3 — Initialize Database

Run migrations to set up the SQLite database and create your admin account:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## Step 4 — Configure Web App in PythonAnywhere Dashboard

1. Go to the **Web** tab in PythonAnywhere.
2. Click **Add a new web app**.
   * If you have a **Free Account**: Select `yourusername.pythonanywhere.com`.
   * If you have a **Paid Account**: Enter your GoDaddy domain (e.g., `www.panchapeethas.org`).
3. Select **Manual Configuration** (do NOT choose Django, we configure it manually for control).
4. Select **Python 3.10** (or whichever version matches your virtual environment).

### 4.1 Update Paths in Web Tab
Once the web app is created, fill in these sections:

* **Source code**: `/home/yourusername/panchapeeta`
* **Working directory**: `/home/yourusername/panchapeeta`
* **Virtualenv**: `/home/yourusername/panchapeeta/venv`

---

## Step 5 — Configure WSGI File (Crucial Step)

Since PythonAnywhere doesn't load environmental variables natively for web workers, we must load `.env` inside the WSGI file.

1. Under the **Web** tab, in the **Code** section, click the link under **WSGI configuration file** (it looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
2. Delete everything inside it, and paste this:

```python
import os
import sys

# Path to your project directory
path = '/home/yourusername/panchapeeta'
if path not in sys.path:
    sys.path.append(path)

# Manually load environment variables from .env
from pathlib import Path
env_path = Path(path) / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                os.environ[key.strip()] = val.strip()

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `yourusername` with your actual PythonAnywhere username).*
3. Click **Save** at the top.

---

## Step 6 — Set Up Static & Media Mappings

To ensure CSS/JS and your temple photos load correctly, configure mappings under the **Web** tab (scroll down to the **Static files** section):

| URL | Path |
|-----|------|
| `/static/` | `/home/yourusername/panchapeeta/staticfiles/` |
| `/media/` | `/home/yourusername/panchapeeta/media/` |

---

## Step 7 — Update GoDaddy DNS

Under your GoDaddy account, locate DNS records for your domain and update:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| **CNAME** | `www` | `webapp-XXXXXX.pythonanywhere.com` *(Copy this host from PythonAnywhere Web Tab)* | 1 Hour |
| **A** | `@` | `35.173.69.207` | 1 Hour |

---

## Step 8 — Enable HTTPS & Reload

1. Under the **Web** tab, scroll to the **Security** section.
2. Toggle **Force HTTPS** to **Enabled**.
3. Scroll to the top of the **Web** tab page and click the green **Reload** button.

🎉 Your application is now live on your GoDaddy custom domain!
