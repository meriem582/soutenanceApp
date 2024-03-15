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

def renderComptes(request):
    return render(request,'comptes.html')

def renderSalles(request):
    return render(request,'salles.html')

def renderConfiguration(request):
    return render(request,'configuration.html')

def renderPlanning(request):
    return render(request,'planning.html')


def renderThemes(request):
    return render(request,'themes.html')