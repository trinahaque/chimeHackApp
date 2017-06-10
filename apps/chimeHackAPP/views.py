from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    response = "Chime Hack App"
    return HttpResponse(response)
