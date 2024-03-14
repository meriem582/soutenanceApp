from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def renderIndex(request):
    return render(request,'index.html')

def renderDashBoardAdmin(request):
    return render(request,'dashBoardAdmin.html')

def renderDashBoardEnseignantt(request):
    return render(request,'dashBoardEnseignant.html')

def renderDashBoardLeader(request):
    return render(request,'dashBoardLeader.html')