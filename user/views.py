import json

from django.http        import JsonResponse
from django.views       import View

from user.models        import UserInfo
from lush.settings      import SECRET_KEY
from lush.settings      import ALGORITHMS

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try :
            if UserInfo.objects.filter(user_id = data['user_id']).exists():
                user = UserInfo.objects.get(user_id = data['user_id'])
                user_password = user.password.encode('utf-8')

                if bcrypt.checkpw(data['password'].encode('utf-8'),user_password):
                    token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHMS)
                    token = token.decode('utf-8')
                    return JsonResponse({"Authorization" : token,'message':"LOGIN SUCCESS"}, status=200)     
                else :
                    return JsonResponse({"message":"WRONG PASSWORD"}, status = 401)
   
            else : 
                return JsonResponse({"message":"WRONG ID"}, status = 401)
                
        except KeyError as e:
            return JsonResponse({'message' : "INVALID_KEYS_".e},status =401)