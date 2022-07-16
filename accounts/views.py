from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegisterUserForm, UserAuthForm

def auth(request):
    if request.method == 'POST':

        if 'login' in request.POST:
            login_form= UserAuthForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('accounts:auth')
        
        if 'signup' in request.POST:
            signup_form = RegisterUserForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('accounts:auth')
        signup_form = RegisterUserForm()
        login_form = UserAuthForm()
    else:
        signup_form = RegisterUserForm()
        login_form = UserAuthForm()
    return render(request, 'accounts/auth.html', {'login_form': login_form, 'signup_form': signup_form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:auth')
