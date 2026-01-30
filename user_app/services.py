from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import Group

def authenticate_and_login_user(request, username,password):
    user = authenticate(request, username=username, password=password)
    if user and user.is_active:
        login(request,user)
    return user


def create_user(username, password, email,first_name, last_name):
    try:
        UserModel = get_user_model()
        user = UserModel(username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name)
        user.set_password(password)
        user.save()
        user.is_staff = True
        user_group = Group.objects.get(name='system_user')
        user.groups.add(user_group)
        user.save()
    except Exception as e:
        print(f'error in creating user - {e}')
        return False
    else:
        return True 