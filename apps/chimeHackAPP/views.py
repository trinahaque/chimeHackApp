from django.shortcuts import render, HttpResponse
from django.contrib import messages
# from .models import User, Problem, Type, Event, Solution, Calendar


# Create your views here.
def index(request):

    return render(request, "chimeHackApp/index.html")
