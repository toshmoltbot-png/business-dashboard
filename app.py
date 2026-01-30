"""
Business Command Center
A real-time dashboard showing health of all Rich's business properties.
"""
import os
import json
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-prod')

# Business configuration
BUSINESSES = [
    {
        'id': 'x2-apparel',
        'name': 'X2-Apparel',
        'url': 'https://x2-apparel.com',
        'description': 'Primary income - Seasonal apparel',
        'priority': 'high',
        'icon': '👕'
    },
    {
        'id': '999rings',
        'name': '999 Championship Rings',
        'url': 'https://999championshiprings.com',
        'description': 'Custom championship rings for youth sports',
        'priority': 'high',
        'icon': '💍'
    },
    {
        'id': 'worcester-flag',
        'name': 'Worcester Flag Football',
        'url': 'https://worcesterflag.com',
        'description': 'Youth NFL FLAG football league',
        'priority': 'high',
        'icon': '🏈'
    },
    {
        'id': 'woo-combine',
        'name': 'Woo-Combine',
        'url': 'https://woo-combine.com',
        'description': 'Athletic combines (needs work)',
        'priority': 'low',
        'icon': '🏃'
    },
    {
        'id': 'getshitdone',
        'name': 'GetShitDone',
        'url': 'https://getshitdone.onrender.com',
        'description': 'Task management system',
        'priority': 'medium',
        'icon': '✅'
    }
]

def check_site_health(business):
    """Check if a site is up and measure response time."""
    result = {
        'id': business['id'],
        'name': business['name'],
        'url': business['url'],
        'description': business['description'],
        'priority': business['priority'],
        'icon': business['icon'],
        'status': 'unknown',
        'response_time_ms': None,
        'error': None,
        'checked_at': datetime.now().isoformat()
    }
    
    try:
        start = datetime.now()
        response = requests.get(
            business['url'], 
            timeout=10, 
            allow_redirects=True,
            headers={'User-Agent': 'BusinessDashboard/1.0'}
        )
        elapsed = (datetime.now() - start).total_seconds() * 1000
        
        result['response_time_ms'] = round(elapsed)
        
        if response.status_code == 200:
            # Check if we got actual content (not just a blank page)
            if len(response.text) > 100:
                result['status'] = 'healthy'
            else:
                result['status'] = 'degraded'
                result['error'] = 'Page loads but has minimal content'
        elif response.status_code in [301, 302]:
            result['status'] = 'redirect'
        else:
            result['status'] = 'error'
            result['error'] = f'HTTP {response.status_code}'
            
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = 'Request timed out (>10s)'
    except requests.exceptions.ConnectionError as e:
        result['status'] = 'down'
        result['error'] = 'Connection failed - site unreachable'
    except requests.exceptions.RequestException as e:
        result['status'] = 'error'
        result['error'] = str(e)[:100]
    
    return result

def check_all_sites():
    """Check all sites in parallel."""
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_site_health, b): b for b in BUSINESSES}
        for future in as_completed(futures):
            results.append(future.result())
    
    # Sort by priority then name
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    results.sort(key=lambda x: (priority_order.get(x['priority'], 3), x['name']))
    
    return results

@app.route('/')
def dashboard():
    """Main dashboard view."""
    sites = check_all_sites()
    
    # Calculate summary stats
    healthy = sum(1 for s in sites if s['status'] == 'healthy')
    issues = sum(1 for s in sites if s['status'] in ['down', 'error', 'timeout'])
    degraded = sum(1 for s in sites if s['status'] == 'degraded')
    
    return render_template('dashboard.html', 
        sites=sites,
        healthy=healthy,
        issues=issues,
        degraded=degraded,
        total=len(sites),
        checked_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/api/status')
def api_status():
    """API endpoint for status checks."""
    sites = check_all_sites()
    return jsonify({
        'status': 'ok',
        'checked_at': datetime.now().isoformat(),
        'sites': sites
    })

@app.route('/api/status/<site_id>')
def api_site_status(site_id):
    """API endpoint for single site status."""
    business = next((b for b in BUSINESSES if b['id'] == site_id), None)
    if not business:
        return jsonify({'error': 'Site not found'}), 404
    
    result = check_site_health(business)
    return jsonify(result)

@app.route('/health')
def health():
    """Health check for Render."""
    return jsonify({
        'status': 'healthy',
        'service': 'business-dashboard',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
