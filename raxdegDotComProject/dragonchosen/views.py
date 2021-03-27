from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Character
import bcrypt

# Create your views here.
def landing(request):
    return redirect('/dragonchosen')

def home(request):
    # CHECK LOGIN
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        context = {
            "user":user,
        }
        return render(request, "home.html", context)
    return render(request, "home.html")

def darkabishai(request):
    return render(request, "darkabishai.html")

# ----------------- LOGIN & REGISTRATION --------------------------
def login(request):
    return render(request, "login.html")

def loginUser(request):
    if(request.method == "POST"):
        errors = User.objects.loginValidator(request.POST)
        if User.objects.errorsPresent(errors, request):
            return redirect('/dragonchosen/login')
        else:
            user = User.objects.filter(username=request.POST['username'])
            user = user[0]
            request.session['userId'] = user.id
            messages.success(request, f"Welcome back, Dragonchosen {user.firstName}. The world was faltering without you.")
            return redirect('/dragonchosen')
    return redirect('/dragonchosen/login')

def register(request):
    if(request.method == "POST"):
        errors = User.objects.registrationValidator(request.POST)
        if User.objects.errorsPresent(errors, request):
            return redirect('/dragonchosen/login')
        else:
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(firstName=request.POST['firstName'],lastName=request.POST['lastName'],username=request.POST['username'],password=hashpw,dm=False)
            request.session['userId'] = newUser.id
            messages.success(request, f"Welcome, Dragonchosen {newUser.firstName}. The fate of the world is in your hands now.")
            return redirect('/dragonchosen')
    return redirect('/dragonchosen/login')

def logout(request):
    request.session.flush()
    return redirect('/dragonchosen/login')

#  --------------------- USER EDITING ---------------------------------------

def editUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    context = {
        "user":user,
    }
    return render(request, "editUser.html", context)

def updateUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    errors = User.objects.updateValidator(request.POST, user.username)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/edit')
    user.firstName = request.POST['firstName']
    user.lastName = request.POST['lastName']
    user.username = request.POST['username']
    user.save()
    messages.success(request, f"Info Updated, Dragonchosen {user.firstName}!")
    return redirect(f"/dragonchosen/edit")

def editPassword(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    context = {
        "user":user,
    }
    return render(request, "editPassword.html", context)

def updatePassword(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    if(request.method == "POST"):
        user = User.objects.get(id=request.session['userId'])
        errors = User.objects.passwordValidator(request.POST, user)
        if User.objects.errorsPresent(errors, request):
            return redirect(f'/dragonchosen/password')
        hashpw = bcrypt.hashpw(request.POST['passwordNew'].encode(), bcrypt.gensalt()).decode()
        user.password = hashpw
        user.save()
        messages.success(request, f"Password Updated, Dragonchosen {user.firstName}!")
    return redirect(f'/dragonchosen/edit')

def deleteUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    user.delete()
    request.session.flush()
    return redirect('/dragonchosen')

