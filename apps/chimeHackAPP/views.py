from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Language, Essay


# Create your views here.
def index(request):
    if "username" in request.session:
        return redirect('/dashboard')
    return render(request, "chimeHackApp/login.html")


def register(request):
    if "username" in request.session:
        return redirect('/dashboard')
    return render(request, "chimeHackApp/register.html")

def registered(request):
    if request.method == "POST":
        result = User.objects.registration(request.POST)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/register')
        else:
            request.session['username']= result[1].username
            request.session['id'] = result[1].id
            return redirect('/dashboard')
    return redirect('/')


def loggedIn(request):
    if request.method == "POST":
        result = User.objects.login(request.POST)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/login')
        else:
            request.session['username']= result[1].username
            request.session['id'] = result[1].id
            return redirect('/dashboard')
    return redirect('/')

def logout(request):
    if 'username' in request.session:
        request.session.pop('username')
        request.session.pop('id')
    return redirect("/")

def dashboard(request):
    if "id" in request.session:
        return render(request, "chimeHackApp/dashboard.html")
    return redirect('/')

def home(request):
    if "id" in request.session:
        user = User.objects.get(id=request.session['id'])
        essays = Essay.objects.filter(user=user)
        context = {
            "essays": essays
        }
        return render(request, "chimeHackApp/home.html", context)
    return redirect('/')

def reflection(request):
    if "id" in request.session:
        return render(request, "chimeHackApp/reflection.html")
    return redirect('/')

def essay(request):
    if request.method == "POST" and "id" in request.session:
        essay = Essay.objects.validateEssay(request.POST, request.session['id'])
        if essay[0] == False:
            for error in essay[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/reflection')
        else:
            return redirect('/dashboard')
