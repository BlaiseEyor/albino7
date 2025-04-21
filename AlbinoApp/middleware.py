from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class NombreVisiteurMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        
        visitor_key = f"visitor_{session_key}"
        
        if not cache.get(visitor_key):
            cache.set(visitor_key, True, timeout=86400)  # Expire après 24h
            if not cache.get("visitor_count"):
                cache.set("visitor_count", 1)
            else:
                cache.incr("visitor_count")
