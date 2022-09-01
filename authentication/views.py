from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'authentication/index.html')

def signup(request):
    

    if request.method=="POST":
        uname=request.POST['uname']
        fname=request.POST['fname']
        lname=request.POST['lname']
        uemail=request.POST['uemail']
        phone=request.POST['phone']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=uname):
            messages.error(request,"User name already exists! Please try some other username")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request,"Passwords didn't match")
            return redirect('signup')

        if not uname.isalnum():
            messages.error(request,"Username name should be alpha_numaric")
            return redirect('signup')
        myuser=User.objects.create_user(uname,uemail,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.phone=phone

        myuser.save()
        messages.success(request,"your account has been sucessfully created") 
        
        return redirect('signin')
    
    return render(request,'authentication/signup.html')

def signin(request):
    
    if request.method=='POST':
        uname=request.POST['uname']
        pass1=request.POST['pass1']

        user= authenticate(username=uname,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"authentication/index.html",{"fname":fname})

        else:
            messages.error(request,"Invaid details")
            return redirect('home')
    
    return render(request,'authentication/signin.html')
    



def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully")
    return redirect('home')
     