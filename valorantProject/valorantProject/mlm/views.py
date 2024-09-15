from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .mlmFunctions import *

# Create your views here.

def mlm(request):
    didModelWork = doModelStuff()
    
    # If the model didn't work
    if not didModelWork:
        return HttpResponse("The model didn't work")
    
    return HttpResponse("The model worked!")