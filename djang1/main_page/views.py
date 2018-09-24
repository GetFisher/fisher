from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect



def main_page_views(request):
    return render(request, 'index.html')



