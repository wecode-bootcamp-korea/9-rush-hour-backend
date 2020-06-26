import json
import bcrypt
import jwt

from django.shortcuts   import render
from django.http        import JsonResponse
from django.views       import View

from user.models        import UserInfo
from lush.settings      import SECRET_KEY

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try :
            if UserInfo.objects.filter(user_id = data['user_id']).exists():
                user = UserInfo.objects.get(user_id = data['user_id'])
                user_password = user.password.encode('utf-8')

                if bcrypt.checkpw(data['password'].encode('utf-8'),user_password):
                    token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = "HS256")
                    token = token.decode('utf-8')
                    return JsonResponse({"Authorization" : token,'message':f'{user.nickname}님 로그인 성공!'}, status=200)     
                else :
                    return JsonResponse({"message":"비밀번호가 틀렸습니다 !"}, status = 401)
   
            else : 
                return JsonResponse({"message":"아이디가 틀렸습니다!"}, status = 401)
                
        except KeyError as e:
            return JsonResponse({'message' : "INVALID_KEYS_".e},status =401)


                



# Create your views here.
