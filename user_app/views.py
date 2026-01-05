from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, SendVideoForm
from videos_app.models import Video

# Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request,user)
#                 return redirect('/admin/')
#     else:
#         form = LoginUserForm()

#     return render(request, 'users/login.html', {'form': form})

class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')



def user_register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            UserModel = get_user_model()
            user = UserModel(username=cd['username'],
                             email=cd['email'],
                             first_name=cd['first_name'],
                             last_name=cd['last_name'])
            
            # user.set_password(form.cleaned_data['password'])
            user.set_password(cd['password'])
            user.save()
            user.is_staff = True
            user_group = Group.objects.get(name='system_user')
            user.groups.add(user_group)
            user.save()
            return redirect('users:login')
            
    else:
        form = RegisterUserForm()

        
    return render(request,'users/register.html',{'form':form})

def user_home(request):
    return render(request, 'users/user/home.html')

def user_profile(request):
    history = Video.objects.filter(user=request.user).values_list()
    print(history)
    return render(request, 'users/user/profile.html', {'history': history})

def send_video(request):
    if request.method == 'POST':
        form = SendVideoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a = Video(link=cd['link'], user=request.user)
            a.save()
    form = SendVideoForm()
    return render(request, 'users/user/send_video.html', {'form': form })

