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


def renderUtilisateur(request):
    recuperation={
        'listeUtilisateur':Utilisateur.objects.all(),
    }
    return render(request,'utilisateur.html',recuperation)    

def renderSalles(request):
    recuperation={
        'listeSalle':Salle.objects.all(),
    }
    return render(request,'salles.html',recuperation)     

def renderConfiguration(request):
    return render(request,'configuration.html')

def renderPlanning(request):
    return render(request,'planning.html')


def renderThemes(request):
    recuperation={
        'listeTheme':Theme.objects.all(),
    }
    return render(request,'themes.html',recuperation)     

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

def login(request):
    email1 = request.POST.get("email")
    password1 = request.POST.get("password")
    type1 = request.POST.get("type_User")
    nuser = Utilisateur.objects.filter(email=email1).first()
    
    if nuser is not None and nuser.password == password1 and nuser.type_User == type1:
        if type1 == "Administrateur":
            return render(request, 'dashBoardAdmin.html')
        elif type1 == "Leader":
            return render(request, 'dashBoardLeader.html')
        elif type1 == "Enseignant":
            return render(request, 'dashBoardEnseignant.html')
    else:
        return HttpResponseRedirect("/")
   