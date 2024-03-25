from django.shortcuts import render
from soutenanceApp.models import Utilisateur,Administrateur,Salle,Occupation_salle,Enseignant,Occupation_Enseignant,Domain_expertise,Theme,Leader,Demande,Evaluation
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

def renderInfoPersonnel(request):
    return render(request,'infoPersonnel.html')


def renderDemandes(request):
    return render(request,'demandes.html')


def renderEvaluation(request):
    return render(request,'evaluation.html')


def renderDemanderThemes(request):
    return render(request,'demanderthemes.html')


def renderDeposerMemoire(request):
    return render(request,'deposerMemoire.html')