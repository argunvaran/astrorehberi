
import json
from .models import UserActivityLog

class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # Log Logic
        # Filter out static, admin, and favicon
        if request.path.startswith('/static') or request.path.startswith('/admin') or 'favicon' in request.path:
            return response

        # Filter out anonymous users if you ONLY want to track registered users
        # But user asked: "siteye girenlerin" (visitors), but also "sessionlari takip edicem" implies login.
        # "Kimler siteye girmis" -> usually implies identity.
        # Let's track everyone but mark user if available.
        # However, to avoid SPAM in logs, maybe only track API calls or Main Page loads.
        
        user = request.user if request.user.is_authenticated else None
        
        # Determine Action Name
        action = "Page View"
        if request.path.startswith('/api/'):
            action = "API Call"
            if 'calculate-chart' in request.path: action = "Calculated Chart"
            elif 'calculate-synastry' in request.path: action = "Checked Compatibility"
            elif 'weekly-forecast' in request.path: action = "Viewed Forecast"
            elif 'login' in request.path: action = "Login Attempt"
            elif 'register' in request.path: action = "Register Attempt"
        
        # Get IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Create Log
        # Only log if user is logged in OR it's a significant action (like calc chart)
        # To prevent DB bloat from random bots hitting index.
        # But user wants to track "who entered site". 
        # Let's log:
        # 1. Any Authenticated User action.
        # 2. Any API call (chart calc) even if anonymous.
        # 3. Index page load.
        
        should_log = False
        if user: should_log = True
        elif request.path == '/': should_log = True
        elif request.path.startswith('/api/'): should_log = True
        
        if should_log and not request.path.endswith('.js') and not request.path.endswith('.css'):
            try:
                UserActivityLog.objects.create(
                    user=user,
                    action=action,
                    path=request.path,
                    method=request.method,
                    ip_address=ip
                )
            except Exception as e:
                print(f"Logging Error: {e}")

        return response
