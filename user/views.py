earom django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
import bcrypt
import jwt
from django.contrib.auth.password_validation import validate_password 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignUp(View):
    def post(self, request):
        data=json.loads(request.body)
        try:
            # validating the userid
            if UserInfo.filter(user_id = data['user_id']).exists():
                return JsonResponse({'message' : 'USER_ID_ALREADY_EXISTS'},status=401)

            # validating the password
            try:
                validate_password(data['password'])
            except ValidationError as e:
                return JsonResponse({'message' : e}, status=401) 
        
            # validating nickname
            if UserInfo.filter(nickname = data['nickname']).exists():
                return JsonResponse({'message': 'NICKNAME_ALREADY_EXISTS'},status=401) 

            # validating email address
            try:
                validate_email(data['email'])
                if UserInfo.filter(email = data['email']).exists():
                    return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'})
            except ValidationError as e:
                return JsonResponse({'message' : e}, status=401)

            # hashing password
            hashed_password = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt() )

            # All necessary info validated, save into DB
            else:
                UserInfo(
                        user_id  =          data['user_id'],
                        password =          hashed_password.decode('utf-8'),
                        nickname =          data['nickname'],
                        email    =          data['email'],
                        name     =          data['name'],
                        phone_no =          data['phone_no'],
                        address  =          data['address'],
                        marketing_agreed =  data['marketing_agreed'],
                        is_guest =          data['is_guest'],
                        created_at =        data['created_at'],
                        update_at =         data['updated_at'],
                        like =              data['like']
                        ).save()
                return JsonResponse({'message': 'SIGN_UP_SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({'message': e}, status=401)
        except Exception as e:
            return JsonResponse({'message': e}, status=401)
