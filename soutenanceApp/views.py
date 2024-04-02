from django.shortcuts import render
from soutenanceApp.models import Utilisateur,Administrateur,Salle,Occupation_salle,Enseignant,Occupation_Enseignant,Domain_expertise,Theme,Leader,Demande,Evaluation,EnseignantDomaineExpertise
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
    e = request.POST["email"]
    ps = request.POST["password"]
    t = request.POST["typeUser"]
    n = request.POST["nom"]
    p = request.POST["prenom"]
    
    nu = Utilisateur(email=e, password=ps, type_User=t, nom=n, prenom=p)
    nu.save()

    user = Utilisateur.objects.get(email=e)
    
    if t == "Administrateur":
        no = Administrateur(email=user)
    elif t == "Enseignant":
        no = Enseignant(email=user)
    elif t == "Leader":
        no = Leader(email=user)
    no.save()
    
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

def renderOccupationSalles(request,id):
    if request.method == 'POST':
        salle1=Salle.objects.get(id=id)
        date_recherche = request.POST.get('date')
        search_results = Occupation_salle.objects.filter(date_occupation=date_recherche,idSalle=salle1)
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

def rendermodifierOccupationSalle(request,ids,id):


    osrech=Occupation_salle.objects.get(ids=ids)
    setinfo={
        'osrechercher':osrech,
    }
    return render(request,'modifierOccupationSalle.html',setinfo) 

def MAJOccupationSalle(request,id,ids):
    newId=request.POST["ids"]
    oldos=Occupation_salle.objects.get(ids=newId)
    d=request.POST["date"]
    hd=request.POST["heure_deb"]
    hf=request.POST["heure_fin"]
    oldos.date_occupation=d

    oldos.heure_debut=hd
    oldos.heure_fin=hf
    oldos.save()
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

def renderDomaineAdmin(request):
    if request.method == 'POST':
        domaine_recherche = request.POST.get('intituler')
        search_results = Domain_expertise.objects.filter(intitule=domaine_recherche)
        return render(request, 'domaineAdmin.html', {'search_results': search_results})
    else:
        listeDomaineAdmin = Domain_expertise.objects.all()  
        return render(request, 'domaineAdmin.html', {'listeDomaineAdmin': listeDomaineAdmin}) 
     
def ajoutDomaineAdmin(request):
    i=request.POST["intitule"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    nda=Domain_expertise(intitule=i,idAdministrateur=admin)
    nda.save()
    return HttpResponseRedirect(reverse("domaineAdmin"))

def suprimerDomaineAdmin(request,id):
    dasup=Domain_expertise.objects.get(id=id)
    dasup.delete()
    return HttpResponseRedirect(reverse("domaineAdmin"))

def rendermodifierDomaineAdmin(request,id):
    drech=Domain_expertise.objects.get(id=id)
    setinfo={
        'darechercher':drech,
    }
    return render(request,'modifierDomaineAdmin.html',setinfo)

def MAJDomaineAdmin(request,id):
    newId=request.POST["id"]
    oldd=Domain_expertise.objects.get(id=newId)
    i=request.POST["intitule"]
    oldd.intitule=i
    oldd.save()
    return HttpResponseRedirect(reverse("domaineAdmin"))

def renderOccupationEnseignant(request):
    if request.method == 'POST':
        eEnseignant=request.session['user_email']
        enseignant1 = Enseignant.objects.get(email=eEnseignant)
        date_recherche = request.POST.get('date')
        search_results = Occupation_Enseignant.objects.filter(date_occupation=date_recherche,idEnseignant=enseignant1)
        return render(request, 'occupationEnseignant.html', {'search_results': search_results})
    else:
        eEnseignant=request.session['user_email']
        enseignant1=Enseignant.objects.get(email=eEnseignant)
        erech=Occupation_Enseignant.objects.filter(idEnseignant=enseignant1)
        setinfo={
        'listeOccupationEnseignant':erech,
        }
        return render(request,'occupationEnseignant.html',setinfo)

def ajoutOccupationEnseignant(request):
    d = request.POST["date"]
    hd = request.POST["heure_deb"]
    hf = request.POST["heure_fin"]
    eEnseignant = request.session['user_email']
    enseignant1 = Enseignant.objects.get(email=eEnseignant)
    noe = Occupation_Enseignant(date_occupation=d, heure_debut=hd, heure_fin=hf, idEnseignant=enseignant1)
    noe.save()
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def suprimerOccupationEnseignant(request,ide):
    soesup=Occupation_Enseignant.objects.get(ide=ide)
    soesup.delete()
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def rendermodifierOccupationEnseignant(request,ide):
    oerech=Occupation_Enseignant.objects.get(ide=ide)
    setinfo={
        'oerechercher':oerech,
    }
    return render(request,'modifierOccupationEnseignant.html',setinfo) 

def MAJOccupationEnseignant(request,ide):
    oldoe=Occupation_Enseignant.objects.get(ide=ide)
    d=request.POST["date"]
    hd=request.POST["heure_deb"]
    hf=request.POST["heure_fin"]
    oldoe.date_occupation=d

    oldoe.heure_debut=hd
    oldoe.heure_fin=hf
    oldoe.save()
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def renderDomaineEnseignant(request):
    eEnseignant = request.session['user_email']
    enseignant = Enseignant.objects.get(email=eEnseignant)
    domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
    context = {
        'listeDomaineEnseignant': domaines_expertise,
        'listeDomaineAdmin': Domain_expertise.objects.all()
    }
    return render(request, 'domaineEnseignant.html', context)

def ajoutDomaineEnseignant(request):
    i=request.POST["intitule"]
    domaine1 = Domain_expertise.objects.get(intitule=i)
    eEnseignant=request.session['user_email']
    enseignant1 = Enseignant.objects.get(email=eEnseignant)
    nde=EnseignantDomaineExpertise(idEnseignant=enseignant1,idDomaineExpertise=domaine1)
    nde.save()
    return HttpResponseRedirect(reverse("domaineEnseignant"))

def suprimerDomaineEnseignant(request,id):
    desup=EnseignantDomaineExpertise.objects.get(id=id)
    desup.delete()
    return HttpResponseRedirect(reverse("domaineEnseignant"))

def renderThemes(request):
    if request.method == 'POST':
        eEnseignant=request.session['user_email']
        enseignant1 = Enseignant.objects.get(email=eEnseignant)
        intitule1 = request.POST.get('intitule')
        search_results = Theme.objects.filter(intitule=intitule1,idEnseignant=enseignant1)
        return render(request, 'themes.html', {'search_results': search_results})
    else:
        eEnseignant = request.session['user_email']
        enseignant = Enseignant.objects.get(email=eEnseignant)
        domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
        trech=Theme.objects.filter(idEnseignant=enseignant)
        context = {
            'listeDomaineEnseignant': domaines_expertise,
            'listeTheme': trech
        }
        return render(request,'themes.html',context)         

def ajoutTheme(request):
    i=request.POST["intitule"]
    d=request.POST["domaine"]
    des=request.POST["description"]
    eEnseignant=request.session['user_email']
    enseignant = Enseignant.objects.get(email=eEnseignant)
    nt=Theme(intitule=i,domaine=d,description=des,idEnseignant=enseignant)
    nt.save()
    return HttpResponseRedirect(reverse("themes"))

def suprimerTheme(request,id):
    tsup=Theme.objects.get(id=id)
    tsup.delete()
    return HttpResponseRedirect(reverse("themes"))

def rendermodifierTheme(request,id):
    eEnseignant = request.session['user_email']
    enseignant = Enseignant.objects.get(email=eEnseignant)
    domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
    trech=Theme.objects.get(id=id)
    context = {
        'listeDomaineEnseignant': domaines_expertise,
        'trechercher':trech,
    }
    return render(request,'modifierTheme.html',context)

def MAJTheme(request,id):
    newId=request.POST["id"]
    oldt=Theme.objects.get(id=newId)
    i=request.POST["intitule"]
    d=request.POST["domaine"]
    des=request.POST["description"]
    oldt.intitule=i
    oldt.domaine=d
    oldt.description=des
    oldt.save()
    return HttpResponseRedirect(reverse("themes"))


def renderDemandes(request):
    eEnseignant=request.session['user_email']
    listeDemande = Demande.objects.filter(idEnseignant=eEnseignant)
    return render(request, 'demandes.html', {'listeDemande': listeDemande})




def renderEvaluation(request):
    return render(request,'evaluation.html')

def renderDemanderThemes(request):
    themes = Theme.objects.all()
    eLeader=request.session['user_email']
    demandes = Demande.objects.filter(idLeader=eLeader)

    return render(request, 'demanderthemes.html', {'themes': themes, 'demandes': demandes})

def ajoutDemande(request,id):
    theme1 = Theme.objects.get(id=id)
    eEnseignant=theme1.idEnseignant.email
    enseignant1=Enseignant.objects.get(email=eEnseignant)
    eLeader=request.session['user_email']
    leader1 = Leader.objects.get(email=eLeader)
    nd=Demande(idTheme=theme1,reponse="",idEnseignant=enseignant1,idLeader=leader1)
    nd.save()
    return HttpResponseRedirect(reverse("demanderthemes"))

def suprimerDemande(request,id):
    dsup=Demande.objects.get(id=id)
    dsup.delete()
    return HttpResponseRedirect(reverse("demanderthemes"))

def validerTheme(request,id):
    demande=Demande.objects.get(id=id)
    eLeader=request.session['user_email']
    leader1 = Leader.objects.get(email=eLeader)
    leader1.idTheme=demande.idTheme
    leader1.idEnseignantEncadrant=demande.idEnseignant
    leader1.save()

      

    return HttpResponseRedirect(reverse("demanderthemes"))

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


def renderConfiguration(request):
    return render(request,'configuration.html')

def renderPlanning(request):
    return render(request,'planning.html')

