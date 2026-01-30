from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .services import authenticate_and_login_user, create_user


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        json_body = json.loads(request.body)
        username = json_body.get('username')
        password = json_body.get('password')
        user = authenticate_and_login_user(request,username,password)
        if user:
            return JsonResponse({'result': 'ok', 'user_id':user.pk})
        else:
            return JsonResponse({'result': 'error', 'user_id':None})

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        json_body = json.loads(request.body)
        username = json_body.get('username')
        password =json_body.get('password')
        email = json_body.get('email')
        first_name = json_body.get('first_name')
        last_name = json_body.get('last_name')
        if create_user(username,password,email,first_name,last_name):
            authenticate_and_login_user(request,username,password)
            return JsonResponse({'result':'ok'})
        else:
            return JsonResponse({'result':'error'})

def user_profile(request):
    # return render(request, 'users/user/profile.html')
    pass

