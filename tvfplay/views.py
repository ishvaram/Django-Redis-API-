from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404, HttpResponseRedirect


# Create your views here.

def index(request):
    return HttpResponse("Pls see the documentation - Redis") 


