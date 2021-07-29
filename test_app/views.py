from django.shortcuts import render,render, HttpResponse

# Create your views here.
def index(request):
    
    return render(request,'index.html')