from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseRedirect
import datetime
import jwt

SECRET_KEY = "yaAzHOU1BF7mtQBkDM9Bf9crzUMaJJzcdbNAH69e6BgiHV_y9gJuiLPG-S-BFZubsYA"

def generate_token(user_id):
    payload = {
        "userid": user_id,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=3)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    valid = False
    payload = None
    message = ""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if "exp" not in payload:
            message = "no exp"
        else:
            valid = True
    except jwt.ExpiredSignatureError:
        message = "expired token"
    except jwt.InvalidTokenError:
        message = "invalid token"
    return { 'valid': valid, 'payload': payload, 'message': message }

def global_context(request):
    return {
        "is_login": getattr(request, "is_login", False)
    }

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        token = request.COOKIES.get('auth')
        white_list = ['/login', '/api/login', '/api/register']
        if path not in white_list:
            is_valid = False
            if token:
                res = verify_token(token)
                if res['valid']:
                    is_valid = True  
            if not is_valid:
                if path.startswith('/api'):
                    return JsonResponse({'message': 'unauthorized'}, status=401)
                else:
                    return HttpResponseRedirect('/login')
            else:
                request.is_login = True