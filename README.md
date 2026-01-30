# Business Command Center 📊

Real-time health monitoring dashboard for Rich's business portfolio.

## Features

- **Live Status Checks** - Monitors all business sites in real-time
- **Visual Health Indicators** - Instant visibility into what's up/down
- **Response Time Tracking** - Know when sites are slow
- **Priority Tagging** - High/medium/low priority sites
- **API Access** - `/api/status` for programmatic access
- **Auto-Refresh** - Updates every 5 minutes

## Sites Monitored

- x2-apparel.com (Primary income)
- 999championshiprings.com (Championship rings)
- worcesterflag.com (Youth flag football)
- woo-combine.com (Athletic combines)
- getshitdone.onrender.com (Task management)

## Deployment

Deployed on Render. Push to main triggers auto-deploy.

## API Endpoints

- `GET /` - Dashboard UI
- `GET /api/status` - JSON status of all sites
- `GET /api/status/<site_id>` - JSON status of specific site
- `GET /health` - Health check for Render

## Local Development

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5001
```

## Built By

Tosh | 2026-01-30
