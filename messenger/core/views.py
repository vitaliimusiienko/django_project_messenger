from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SingUpForm,LoginForm


def homepage(request):
    return render(request, 'core/homepage.html')

def signup_user(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            return redirect('homepage')
    
    else:
        form = SingUpForm
    return render(request, 'core/signup.html', {'form':form})
        
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('homepage')
                
                else:
                    redirect('login')
            else:
                redirect('login')
        else:
            redirect('login')
    else:
        form = LoginForm
        
    return render(request, 'core/login.html', {'form':form})

def logout_user(request):
    logout(request)
    
    return redirect('homepage')
