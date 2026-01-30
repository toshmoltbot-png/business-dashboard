# Deploy to Render

## Quick Deploy (1 minute)

1. Go to https://dashboard.render.com/

2. Click **"New +"** → **"Web Service"**

3. Connect GitHub repo: `toshmoltbot-png/business-dashboard`

4. Settings will auto-fill from `render.yaml`:
   - Name: `business-dashboard`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30`

5. Click **"Create Web Service"**

6. Wait ~2 minutes for deploy

7. Your dashboard is live at: `https://business-dashboard.onrender.com`

## After Deployment

- Dashboard auto-refreshes every 5 minutes
- Check `/api/status` for JSON data
- Add to bookmarks for quick access

## Updating

Push to GitHub → Render auto-deploys

```bash
cd /Users/tosh/clawd/business-dashboard
git add -A && git commit -m "Update" && git push
```
