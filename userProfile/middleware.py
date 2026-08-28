

class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if '/api/auth/login' in request.path or '/api/auth/refresh' in request.path:
            return self.get_response(request)
        
        token = request.COOKIES.get('access_token')
        
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            
        response = self.get_response(request)
        return response