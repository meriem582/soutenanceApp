from django.shortcuts import render
from soutenanceApp.models import Utilisateur,Administrateur,Salle,Occupation_salle,Enseignant,Occupation_Enseignant,Domain_expertise,Theme,Leader,Demande,Evaluation
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def renderIndex(request):
    return render(request,'index.html')

def renderUtilisateur(request):
    if request.method == 'POST':
        email_recherche = request.POST.get('emailr')
        search_results = Utilisateur.objects.filter(email=email_recherche)
        return render(request, 'utilisateur.html', {'search_results': search_results})
    else:
        listeUtilisateur = Utilisateur.objects.all()  
        return render(request, 'utilisateur.html', {'listeUtilisateur': listeUtilisateur})    

def ajoutUtilisateur(request):
    e=request.POST["email"]
    p=request.POST["password"]
    t=request.POST["typeUser"]
    n=request.POST["nom"]
    p=request.POST["prenom"]
    nu=Utilisateur(email=e,password=p,type_User=t,nom=n,prenom=p)
    nu.save()
    return HttpResponseRedirect(reverse("utilisateur"))

def suprimerUtilisateur(request,email):
    usup=Utilisateur.objects.get(email=email)
    usup.delete()
    return HttpResponseRedirect(reverse("utilisateur"))

def rendermodifierUtilisateur(request,email):
    urech=Utilisateur.objects.get(email=email)
    setinfo={
        'urechercher':urech,
    }
    return render(request,'modifierUtilisateur.html',setinfo)

def MAJUtilisateur(request,email):
    newEmail=request.POST["email"]
    oldu=Utilisateur.objects.get(email=newEmail)
    ps=request.POST["password"]
    n=request.POST["nom"]
    p=request.POST["prenom"]
    oldu.password=ps
    oldu.nom=n
    oldu.prenom=p
    oldu.save()
    return HttpResponseRedirect(reverse("utilisateur"))

def rechercheUtilisateur(request):
    email=request.POST["emailr"]
    urech=Utilisateur.objects.get(email=email)
    setinfo={
        'urechercher':urech,
    }
    return render(request,'modifierUtilisateur.html',setinfo)


def renderSalles(request):
    if request.method == 'POST':
        bloc_recherche = request.POST.get('bloc')
        search_results = Salle.objects.filter(num_bloc=bloc_recherche)
        return render(request, 'salles.html', {'search_results': search_results})
    else:
        listeSalle = Salle.objects.all()  
        return render(request, 'salles.html', {'listeSalle': listeSalle}) 


def ajoutSalle(request):
    b=request.POST["bloc"]
    s=request.POST["salle"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    ns=Salle(num_bloc=b,num_salle=s,idAdministrateur=admin)
    ns.save()
    return HttpResponseRedirect(reverse("salles"))

    
def ajoutSalle(request):
    b=request.POST["bloc"]
    s=request.POST["salle"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    ns=Salle(num_bloc=b,num_salle=s,idAdministrateur=admin)
    ns.save()
    return HttpResponseRedirect(reverse("salles"))

def suprimerSalle(request,id):
    ssup=Salle.objects.get(id=id)
    ssup.delete()
    return HttpResponseRedirect(reverse("salles"))

def rendermodifierSalle(request,id):
    srech=Salle.objects.get(id=id)
    setinfo={
        'srechercher':srech,
    }
    return render(request,'modifierSalle.html',setinfo)

def MAJSalle(request,id):
    newId=request.POST["id"]
    olds=Salle.objects.get(id=newId)
    numb=request.POST["bloc"]
    nums=request.POST["salle"]
    olds.num_bloc=numb
    olds.num_salle=nums
    olds.save()
    return HttpResponseRedirect(reverse("salles"))

def rechercheSalle(request):
    bloc1=request.POST["bloc"]
    srech=Salle.objects.get(bloc=bloc1)
    setinfo={
        'srechercher':srech,
    }
    return render(request,'modifierSalle.html',setinfo)



def renderOccupationSalles(request,id):
    if request.method == 'POST':
        date_recherche = request.POST.get('date')
        search_results = Occupation_salle.objects.filter(date_occupation=date_recherche)
        return render(request, 'occupationSalle.html', {'search_results': search_results})
    else:
        salle1=Salle.objects.get(id=id)
        srech=Occupation_salle.objects.filter(idSalle=salle1)
        setinfo={
        'listeOccupationSalle':srech,
        }
        return render(request,'occupationSalle.html',setinfo)



def ajoutOccupationSalle(request, id):
    d = request.POST["date"]
    hd = request.POST["heure_deb"]
    hf = request.POST["heure_fin"]
    eAdmin = request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    salle1 = Salle.objects.get(id=id)
    nos = Occupation_salle(date_occupation=d, heure_debut=hd, heure_fin=hf, idSalle=salle1, idAdministrateur=admin)
    nos.save()
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))


def suprimerOccupationSalle(request,id,ids):
    sosup=Occupation_salle.objects.get(ids=ids)
    sosup.delete()
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

     
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
        request.session['user_email'] = email1  # Stocker l'e-mail dans la session
        if type1 == "Administrateur":
            return render(request, 'dashBoardAdmin.html')
        elif type1 == "Leader":
            return render(request, 'dashBoardLeader.html')
        elif type1 == "Enseignant":
            return render(request, 'dashBoardEnseignant.html')
    else:
        return HttpResponseRedirect("/")

   