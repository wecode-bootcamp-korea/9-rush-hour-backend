import json
import bcrypt
import jwt

from django.http                             import JsonResponse
from django.views                            import View
from django.contrib.auth.password_validation import validate_password 
from django.core.validators                  import validate_email
from django.core.exceptions                  import ValidationError

from user.models                             import UserInfo
from lush.settings                           import SECRET_KEY
from lush.settings                           import ALGORITHMS

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try :
            if UserInfo.objects.filter(user_id = data['user_id']).exists():
                user = UserInfo.objects.get(user_id = data['user_id'])
                user_password = user.password.encode('utf-8')

                if bcrypt.checkpw(data['password'].encode('utf-8'),user_password):
                    token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHMS).decode('utf-8')
                    return JsonResponse({'Authorization' : token,'message':'LOGIN SUCCESS'}, status=200)     
                
                return JsonResponse({'message':'WRONG PASSWORD'}, status = 401)
   
            return JsonResponse({'message':'WRONG ID'}, status = 401)
                
        except KeyError as e:
            return JsonResponse({'message' : 'INVALID_KEYS_'.e},status =401)

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
