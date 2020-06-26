import json
import jwt

from django.views   import View
from django.http    import JsonResponse

from user.models    import UserInfo
from lush.settings  import SECRET_KEY

def login_decorator(func):
    def wrapper(self, request):
        access_token    = request.headers.get("Authorization")
        decoded_token   = jwt.decode(access_token, 'secret', algorithms='HS256')

        if UserInfo.objects.filter(user_id = decoded_token['id']).exists():
            valid_user   = UserInfo.objects.get(user_id = decoded_token['id'])
            request.user = valid_user
            return func(self,request)
    
        else:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)

    return wrapper
