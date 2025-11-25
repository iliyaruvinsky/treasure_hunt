# How to Start/Initialize the Treasure Hunt Analyzer Servers

## Quick Start (3 Steps)

### Step 1: Navigate to Project Directory

Open PowerShell or Command Prompt and run:

```powershell
cd /d "G:\My Drive\SW_PLATFORM\4. MARKETING\PRESENTATIONS\CURRENT\14. Treasure Hunting\treasure-hunt-analyzer"
```

**Note:** If you're already in the project directory, skip this step.

### Step 2: Start All Services

Run one of these commands (depending on your Docker version):

**For newer Docker versions (recommended):**
```powershell
docker compose up -d
```

**For older Docker versions:**
```powershell
docker-compose up -d
```

**What this does:**
- Starts PostgreSQL database
- Starts Backend API server (port 8080)
- Starts Frontend web server (port 3001)
- Runs everything in the background (`-d` flag)

### Step 3: Wait and Verify (30-60 seconds)

Wait about 30-60 seconds for services to start, then check status:

```powershell
docker compose ps
```

**Expected output:**
- `tha-postgres`: Status should show `Up` and `(healthy)`
- `tha-backend`: Status should show `Up` and `(healthy)`
- `tha-frontend`: Status should show `Up`

## Access Your Application

Once all services show "Up":

- **Frontend (Web UI)**: http://localhost:3001
- **Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## Troubleshooting

### If services don't start:

1. **Check Docker is running:**
   ```powershell
   docker --version
   ```
   If this fails, start Docker Desktop.

2. **Check for port conflicts:**
   - Port 8080 (backend) or 3001 (frontend) might be in use
   - Check what's using them: `netstat -ano | findstr :8080`

3. **View logs for errors:**
   ```powershell
   docker compose logs backend
   docker compose logs frontend
   ```

4. **Rebuild if needed:**
   ```powershell
   docker compose up -d --build
   ```

### If you see "unhealthy" status:

Wait a bit longer (up to 2 minutes). Health checks need time to pass.

### To stop all services:

```powershell
docker compose down
```

### To restart services:

```powershell
docker compose restart
```

## Initialize Database (First Time Only)

If this is your first time running the system, initialize the database:

```powershell
docker compose exec backend python -m app.utils.init_db
```

This creates all necessary database tables.

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop all services |
| `docker compose ps` | Check service status |
| `docker compose logs` | View all logs |
| `docker compose logs backend` | View backend logs only |
| `docker compose restart` | Restart all services |
| `docker compose up -d --build` | Rebuild and start |

## Need Help?

- Check logs: `docker compose logs`
- Check status: `docker compose ps`
- Verify Docker: `docker --version`
- Verify ports: Open http://localhost:8080/health in browser

