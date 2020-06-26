import json
import bcrypt
import jwt

from django.views                            import View
from django.http                             import JsonResponse
from django.contrib.auth.password_validation import validate_password 
from django.core.validators                  import validate_email
from django.core.exceptions                  import ValidationError

from user.models                             import UserInfo

class SignUp(View):
    def post(self, request):
        data=json.loads(request.body)
        try:
            # hashing password
            hashed_password = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt() )

            # if userid already exists in the db
            if UserInfo.objects.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'USER_ID_ALREADY_EXISTS'},status=401)
            
            # validating the password
            try:
                validate_password(data['password'])
            except ValidationError:
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=401) 
                        
            # if nickname already exists in the db
            if UserInfo.objects.filter(nickname = data['nickname']).exists():
                return JsonResponse({'message': 'NICKNAME_ALREADY_EXISTS'},status=401) 
            
            # validating email address
            try:
                validate_email(data['email'])
            except:
                return JsonResponse({'message': 'INVALID_EMAIL'})

            # if email already exists in the db
            if UserInfo.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'})
                
            # All necessary info validated, save into DB
            else:
                UserInfo(
                        user_id          = data['user_id'],
                        password         = hashed_password.decode('utf-8'),
                        nickname         = data['nickname'],
                        email            = data['email'],
                        name             = data['name'],
                        phone_number     = data['phone_number'],
                        address          = data['address']
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=401)
