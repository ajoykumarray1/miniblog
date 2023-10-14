from django.shortcuts import render,redirect
from django.contrib import messages
from blog.models import Post
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
#home...........
def home(request):
    posts = Post.objects.all()
    return render(request,'home.html',{'posts':posts})

#contact
@login_required
def contact(request):
    return render(request,'contact.html')

#dashboard
@login_required
def dashboard(request):
    posts=Post.objects.all()
    return render(request,'dashboard.html',{'posts':posts})

#Added Post
@login_required
def addPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request,"You have successfully posted data")
            return redirect('dashboard')
        else:
           messages.error(request,"Invalid title or descriptios") 
    else:
      form=PostForm
    return render(request,'addpage.html',{'form':form})

#Delete Post
def deletePost(request,id):
    pk=Post.objects.get(id=id)
    pk.delete()
    return redirect('dashboard')

#Update Post
def updatePost(request,id):
    if request.method=='POST':
        pi=Post.objects.get(id=id)
        form=PostForm(request.POST,instance=pi)
        if form.is_valid:
            form.save()
            messages.success(request,"Successfully Updated")
            return redirect('dashboard')
    else:
        pi=Post.objects.get(id=id)
        form=PostForm(instance=pi)
    return render(request,'updatepost.html',{'form':form})


#SignUpPage
def signupPage(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! You have become a author ✔✔👍')
            form.save()
        else:
            messages.error(request,"InValid Password or Username or This username has been taken.")
    else:
        form = SignUpForm()

    return render(request,'signup.html',{'form':form})
    # return render(request,'signup.html')

#about
def about(request):
    return render(request,'about.html')

#login
def login(request):
    # form = LoginForm()
    if not request.user.is_authenticated:
        if request.method =='POST':
            form = LoginForm(request=request,data= request.POST)
            if form.is_valid:
                uname = request.POST.get('username')
                upass = request.POST.get('password')
                user = auth.authenticate(request,username = uname,password = upass)
                if user != None:
                    auth.login(request,user)
                    messages.success(request,'You have successfully logged in 😁😁👍')
                    return redirect('home')
                else:
                    messages.error(request,'Username or password invalid')
                    return redirect('login')
        else:
            form = LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        return redirect('home')

#logout
def logoutPage(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')