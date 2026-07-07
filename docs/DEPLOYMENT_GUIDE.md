# Panchapeethas — CI/CD & Deployment Guide

## Branch Strategy

| Branch   | Purpose                        | Auto-Deploys? |
|----------|--------------------------------|---------------|
| **`dev`**  | Your daily work branch         | ❌ No          |
| **`main`** | Production branch (live site)  | ✅ Yes         |

---

## How Deployment Works

```
Push code to `dev` (no deployment)
         ↓
Create Pull Request: dev → main (review changes)
         ↓
Merge PR (deployment triggers automatically)
         ↓
GitHub Actions SSH into EC2
         ↓
git pull → pip install requirements
         ↓
systemctl restart panchapeethas
         ↓
ExecStartPre automatically runs:
  1. manage.py migrate (PostgreSQL via .env)
  2. manage.py collectstatic
         ↓
Gunicorn starts → Nginx restarted
         ↓
✅ Site is live at https://panchapeeta.org
```

---

## Daily Development Workflow

### 1. Work on `dev` branch (no deployment happens)

```bash
# Make sure you're on dev
git checkout dev

# Make your changes, then commit and push
git add .
git commit -m "your commit message"
git push
```

### 2. Deploy to Production (when ready)

**Option A — Via GitHub (Recommended)**
1. Go to https://github.com/Gurucharan-G/panchapeeta
2. Click **"Compare & pull request"** or go to **Pull Requests → New**
3. Set: `base: main` ← `compare: dev`
4. Review your changes
5. Click **"Merge pull request"**
6. Deployment happens automatically (~30 seconds)

**Option B — Via Terminal (Quick deploy)**
```bash
git checkout main
git merge dev
git push
git checkout dev
```

---

## What Happens During Deployment (GitHub Actions)

The workflow file is at `.github/workflows/deploy.yml`. On every push to `main`:

1. **SSH into EC2** — Uses `appleboy/ssh-action` with secrets `AWS_HOST` and `AWS_PRIVATE_KEY`
2. **Pull latest code** — `git pull origin main`
3. **Install dependencies** — `pip install -r requirements.txt`
4. **Restart service** — `systemctl restart panchapeethas`
   - This automatically runs `manage.py migrate` (against PostgreSQL RDS)
   - This automatically runs `manage.py collectstatic`
5. **Restart Nginx** — `systemctl restart nginx`
6. **Verify** — Checks that the service is active

---

## Systemd Service Configuration

The service file at `/etc/systemd/system/panchapeethas.service` includes:

```ini
[Service]
EnvironmentFile=/opt/panchapeethas/app/.env    # Loads DB credentials
ExecStartPre=...manage.py migrate --noinput    # Auto-migrate before start
ExecStartPre=...manage.py collectstatic --noinput  # Auto-collect static files
ExecStart=...gunicorn ...                      # Start Gunicorn
```

**Key:** The `EnvironmentFile` directive ensures Django always connects to the **PostgreSQL RDS database** (not the local SQLite fallback).

---

## GitHub Secrets Required

These must be set at: **GitHub Repo → Settings → Secrets and variables → Actions**

| Secret            | Value                         |
|-------------------|-------------------------------|
| `AWS_HOST`        | `52.55.134.185`               |
| `AWS_PRIVATE_KEY` | Contents of `panchapeethas-key.pem` |

---

## Troubleshooting

### Check deployment status
Go to: https://github.com/Gurucharan-G/panchapeeta/actions

### If deployment fails, SSH manually
```bash
ssh -i panchapeethas-key.pem ubuntu@52.55.134.185

# Check service status
sudo systemctl status panchapeethas

# Check logs
sudo journalctl -u panchapeethas -n 50 --no-pager

# Manual restart
sudo systemctl restart panchapeethas
```

### If migrations fail on PostgreSQL
```bash
# Run migrations with correct DB connection
sudo -u panchapeethas bash -c 'source /opt/panchapeethas/app/.env && cd /opt/panchapeethas/app && venv/bin/python manage.py migrate'
```
