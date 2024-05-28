from django.shortcuts import redirect, render
from soutenanceApp.models import Utilisateur,Administrateur,Salle,Occupation_salle,Enseignant,Occupation_Enseignant,Domain_expertise,Theme,Leader,Demande,Evaluation,EnseignantDomaineExpertise,Parametre
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from datetime import datetime, timedelta, time
import random
from collections import defaultdict
from weasyprint import HTML , CSS
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



def renderIndex(request):
    return render(request,'index.html')

def renderDashBoardAdmin(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    return render(request,'dashBoardAdmin.html', {'user': user})
    

def renderDashBoardEnseignant(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    return render(request,'dashBoardEnseignant.html', {'user': user})

def renderDashBoardLeader(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    return render(request,'dashBoardLeader.html', {'user': user})



def enseignant_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        eUser=request.session['user_email']
        user = Utilisateur.objects.get(email=eUser)

        if  user.type_User == 'Enseignant':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès non autorisé. Vous devez être enseignant pour accéder à cette page.")
            return redirect('/login/')  # Redirige vers la page de connexion
    return wrapper_func



@enseignant_required
def renderParamètres(request):
    eUser = request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    return render(request, 'paramètres.html', {'user': user})

def renderUtilisateur(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        email_recherche = request.POST.get('emailr')
        search_results = Utilisateur.objects.filter(email=email_recherche)
        return render(request, 'utilisateur.html', {'search_results': search_results,'user': user})
    else:
        listeUtilisateur = Utilisateur.objects.all()  
        return render(request, 'utilisateur.html', {'listeUtilisateur': listeUtilisateur,'user': user}) 


def ajoutGrade(request):
    if request.method == 'POST':
        # Assurez-vous que l'utilisateur est connecté
        if 'user_email' in request.session:
            # Récupérez l'adresse e-mail de l'utilisateur connecté
            email = request.session['user_email']
            
            try:
                # Récupérez l'enseignant associé à cette adresse e-mail
                enseignant = Enseignant.objects.get(email=email)
            except Enseignant.DoesNotExist:
                # Gérer le cas où l'enseignant n'existe pas
                messages.error(request, "Impossible de trouver votre profil d'enseignant.")
                return redirect('paramètres')  # Rediriger vers une page appropriée
            
            # Mettez à jour le grade de l'enseignant avec la valeur du formulaire
            grade = request.POST.get('grade')
            enseignant.grade = grade
            enseignant.save()

            # Afficher un message de succès ou de confirmation
            messages.success(request, "Votre grade a été mis à jour avec succès.")
            return redirect('paramètres')  # Rediriger vers une page appropriée
        else:
            # Gérer le cas où l'utilisateur n'est pas connecté
            messages.error(request, "Bug.")
            return redirect('paramètres')  # Rediriger vers une page appropriée
    else:
        # Gérer le cas où la méthode de la requête n'est pas POST
        messages.error(request, "Méthode de requête non autorisée.")
        return redirect('paramètres')  # Rediriger vers une page appropriée

# def ajoutGrade(request):
#     if request.method == "POST":
#         # Récupérer l'adresse e-mail de l'utilisateur connecté depuis la session
#         user_email = request.session.get('user_email')
#         # Récupérer l'utilisateur à partir de l'adresse e-mail
#         user = Utilisateur.objects.get(email=user_email)
        
#         # Récupérer le grade à partir des données du formulaire
#         grade = request.POST.get("grade")
        
#         # Enregistrer le grade pour l'utilisateur connecté
#         user.grade = grade
#         user.save()

#         # Rediriger l'utilisateur vers une page de confirmation ou une autre page appropriée
#         messages.success(request, "Votre grade a été mis à jour avec succès.")
#         return HttpResponseRedirect(reverse("paramètres"))
#     else:
#         # Gérer le cas où la méthode de requête n'est pas POST
#         return messages.error("Méthode non autorisée")


def ajoutUtilisateur(request):
    e = request.POST["email"]
    ps = request.POST["password"]
    t = request.POST["typeUser"]
    n = request.POST["nom"]
    p = request.POST["prenom"]
    nu = Utilisateur(email=e, password=ps, type_User=t, nom=n, prenom=p)
    nu.save()
    messages.success(request,"Utilisateur ajouté avec succès")
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
    messages.success(request,"Utilisateur supprimé avec succès")
    return HttpResponseRedirect(reverse("utilisateur"))

def rendermodifierUtilisateur(request,email):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    urech=Utilisateur.objects.get(email=email)
    setinfo={
        'urechercher':urech,
        'user': user,
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
    messages.success(request,"Utilisateur modifié avec succès")
    return HttpResponseRedirect(reverse("utilisateur"))
    


def renderSalles(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        bloc_recherche = request.POST.get('bloc')
        search_results = Salle.objects.filter(num_bloc=bloc_recherche)
        return render(request, 'salles.html', {'search_results': search_results,'user': user})
    else:
        listeSalle = Salle.objects.all()  
        return render(request, 'salles.html', {'listeSalle': listeSalle,'user': user}) 
 
def ajoutSalle(request):
    b=request.POST["bloc"]
    s=request.POST["salle"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    ns=Salle(num_bloc=b,num_salle=s,idAdministrateur=admin)
    ns.save()
    messages.success(request,'Salle ajoutée avec succès')
    return HttpResponseRedirect(reverse("salles"))
  

def suprimerSalle(request,id):
    ssup=Salle.objects.get(id=id)
    ssup.delete()
    messages.success(request,'Salle supprimée avec succès')
    return HttpResponseRedirect(reverse("salles"))

def rendermodifierSalle(request,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    srech=Salle.objects.get(id=id)
    setinfo={
        'srechercher':srech,
        'user': user,
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
    messages.success(request,'Salle modifiée avec succès')
    return HttpResponseRedirect(reverse("salles"))

def renderOccupationSalles(request,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        salle1=Salle.objects.get(id=id)
        date_recherche = request.POST.get('date')
        search_results = Occupation_salle.objects.filter(date_occupation=date_recherche,idSalle=salle1)
        return render(request, 'occupationSalle.html', {'search_results': search_results,'user': user})
    else:
        salle1=Salle.objects.get(id=id)
        srech=Occupation_salle.objects.filter(idSalle=salle1)
        setinfo={
            'listeOccupationSalle':srech,
            'user': user,
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
    messages.success(request,"Occupation ajoutée avec succès")
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

def suprimerOccupationSalle(request,id,ids):
    sosup=Occupation_salle.objects.get(ids=ids)
    sosup.delete()
    messages.success(request,"Occupation supprimée avec succès")
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

def rendermodifierOccupationSalle(request,ids,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    osrech=Occupation_salle.objects.get(ids=ids)
    setinfo={
        'osrechercher':osrech,
        'user': user,
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
    messages.success(request,"Occupation modifiée avec succès")
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

def renderDomaineAdmin(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        domaine_recherche = request.POST.get('intituler')
        search_results = Domain_expertise.objects.filter(intitule=domaine_recherche)
        return render(request, 'domaineAdmin.html', {'search_results': search_results,'user': user})
    else:
        listeDomaineAdmin = Domain_expertise.objects.all()  
        return render(request, 'domaineAdmin.html', {'listeDomaineAdmin': listeDomaineAdmin,'user': user}) 
     
def ajoutDomaineAdmin(request):
    i=request.POST["intitule"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    nda=Domain_expertise(intitule=i,idAdministrateur=admin)
    nda.save()
    messages.success(request,"Domaine ajouté avec succès")
    return HttpResponseRedirect(reverse("domaineAdmin"))

def suprimerDomaineAdmin(request,id):
    dasup=Domain_expertise.objects.get(id=id)
    dasup.delete()
    messages.success(request,"Domaine supprimé avec succès")
    return HttpResponseRedirect(reverse("domaineAdmin"))

def rendermodifierDomaineAdmin(request,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    drech=Domain_expertise.objects.get(id=id)
    setinfo={
        'darechercher':drech,
        'user': user,
    }
    return render(request,'modifierDomaineAdmin.html',setinfo)

def MAJDomaineAdmin(request,id):
    newId=request.POST["id"]
    oldd=Domain_expertise.objects.get(id=newId)
    i=request.POST["intitule"]
    oldd.intitule=i
    oldd.save()
    messages.success(request,"Domaine modifié avec succès")
    return HttpResponseRedirect(reverse("domaineAdmin"))

def renderOccupationEnseignant(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        eEnseignant=request.session['user_email']
        enseignant1 = Enseignant.objects.get(email=eEnseignant)
        date_recherche = request.POST.get('date')
        search_results = Occupation_Enseignant.objects.filter(date_occupation=date_recherche,idEnseignant=enseignant1)
        return render(request, 'occupationEnseignant.html', {'search_results': search_results,'user': user})
    else:
        eEnseignant=request.session['user_email']
        enseignant1=Enseignant.objects.get(email=eEnseignant)
        erech=Occupation_Enseignant.objects.filter(idEnseignant=enseignant1)
        setinfo={
        'listeOccupationEnseignant':erech,
        'user': user,
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
    messages.success(request,"Occupation ajoutée avec succès")
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def suprimerOccupationEnseignant(request,ide):
    soesup=Occupation_Enseignant.objects.get(ide=ide)
    soesup.delete()
    messages.success(request,"Occupation supprimée avec succès")
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def rendermodifierOccupationEnseignant(request,ide):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    oerech=Occupation_Enseignant.objects.get(ide=ide)
    setinfo={
        'oerechercher':oerech,
        'user': user,
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
    messages.success(request,"Occupation modifiée avec succès")
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def renderDomaineEnseignant(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    eEnseignant = request.session['user_email']
    enseignant = Enseignant.objects.get(email=eEnseignant)
    domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
    context = {
        'listeDomaineEnseignant': domaines_expertise,
        'listeDomaineAdmin': Domain_expertise.objects.all(),
        'user': user,
    }
    return render(request, 'domaineEnseignant.html', context)

def ajoutDomaineEnseignant(request):
    i=request.POST["intitule"]
    domaine1 = Domain_expertise.objects.get(intitule=i)
    eEnseignant=request.session['user_email']
    enseignant1 = Enseignant.objects.get(email=eEnseignant)
    nde=EnseignantDomaineExpertise(idEnseignant=enseignant1,idDomaineExpertise=domaine1)
    nde.save()
    messages.success(request,"Domaine ajouté avec succès")
    return HttpResponseRedirect(reverse("domaineEnseignant"))

def suprimerDomaineEnseignant(request,id):
    desup=EnseignantDomaineExpertise.objects.get(id=id)
    desup.delete()
    messages.success(request,"Domaine supprimé avec succès")
    return HttpResponseRedirect(reverse("domaineEnseignant"))

def renderThemes(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        eEnseignant=request.session['user_email']
        enseignant1 = Enseignant.objects.get(email=eEnseignant)
        intitule1 = request.POST.get('intitule')
        search_results = Theme.objects.filter(intitule=intitule1,idEnseignant=enseignant1)
        return render(request, 'themes.html', {'search_results': search_results,'user': user})
    else:
        eEnseignant = request.session['user_email']
        enseignant = Enseignant.objects.get(email=eEnseignant)
        domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
        trech=Theme.objects.filter(idEnseignant=enseignant)
        context = {
            'listeDomaineEnseignant': domaines_expertise,
            'listeTheme': trech,
            'user': user,
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
    messages.success(request,"Thème ajouté avec succès")
    return HttpResponseRedirect(reverse("themes"))

def suprimerTheme(request,id):
    tsup=Theme.objects.get(id=id)
    tsup.delete()
    messages.success(request,"Thème supprimé  avec succès")
    return HttpResponseRedirect(reverse("themes"))

def rendermodifierTheme(request,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    eEnseignant = request.session['user_email']
    enseignant = Enseignant.objects.get(email=eEnseignant)
    domaines_expertise = enseignant.enseignantdomaineexpertise_set.all()
    trech=Theme.objects.get(id=id)
    context = {
        'listeDomaineEnseignant': domaines_expertise,
        'trechercher':trech,
        'user': user,
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
    messages.success(request,"Thème modifié avec succès")
    return HttpResponseRedirect(reverse("themes"))

def renderDemandes(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    eEnseignant=request.session['user_email']
    listeDemande = Demande.objects.filter(idEnseignant=eEnseignant)
    return render(request, 'demandes.html', {'listeDemande': listeDemande,'user': user})

def renderDemanderThemes(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    themes = Theme.objects.all()
    eLeader=request.session['user_email']
    demandes = Demande.objects.filter(idLeader=eLeader).exclude(reponse='Accepté')
    demandesAccepter = Demande.objects.filter(idLeader=eLeader, reponse='Accepté')
    return render(request, 'demanderthemes.html', {'themes': themes, 'demandes': demandes, 'demandesAccepter':demandesAccepter,'user': user})

def ajoutDemande(request,id):
    theme1 = Theme.objects.get(id=id)
    eEnseignant=theme1.idEnseignant.email
    enseignant1=Enseignant.objects.get(email=eEnseignant)
    eLeader=request.session['user_email']
    leader1 = Leader.objects.get(email=eLeader)
    nd=Demande(idTheme=theme1,reponse="",idEnseignant=enseignant1,idLeader=leader1)
    nd.save()
    messages.success(request,"Demande envoyée avec succès")
    return HttpResponseRedirect(reverse("demanderthemes"))

def suprimerDemande(request,id):
    dsup=Demande.objects.get(id=id)
    dsup.delete()
    messages.success(request,"Demande supprimée avec succès")
    return HttpResponseRedirect(reverse("demanderthemes"))

def validerTheme(request,id):
    demande=Demande.objects.get(id=id)
    eLeader=request.session['user_email']
    leader1 = Leader.objects.get(email=eLeader)
    leader1.idTheme=demande.idTheme
    leader1.idEnseignantEncadrant=demande.idEnseignant
    leader1.save()
    messages.success(request,"Thème validé avec succès")
    return HttpResponseRedirect(reverse("demanderthemes"))

def renderDeposerMemoire(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    eLeader=request.session['user_email']
    leader = Leader.objects.get(email=eLeader)
    return render(request, 'deposerMemoire.html', {'leader': leader,'user': user})

def ajoutMemoire(request):
    if request.method == 'POST':
        fichier_pdf = request.FILES['memoire']
        eLeader=request.session['user_email']
        leader = Leader.objects.get(email=eLeader)
        leader.memoire = fichier_pdf.read()
        leader.save()
        messages.success(request,"Mémoire ajouté avec succès")
        return HttpResponseRedirect(reverse("deposerMemoire"))
    return render(request, 'deposerMemoire.html')

def login(request):
    email1 = request.POST.get("email")
    password1 = request.POST.get("password")
    type1 = request.POST.get("type_User")
    nuser = Utilisateur.objects.filter(email=email1).first()
    if nuser is not None and nuser.password == password1 and nuser.type_User == type1:
        request.session['user_email'] = email1
        eUser=request.session['user_email']
        user = Utilisateur.objects.get(email=eUser)
        if type1 == "Administrateur":
            return render(request, 'dashBoardAdmin.html',{'user': user})
        elif type1 == "Leader":
            return render(request, 'dashBoardLeader.html',{'user': user})
        elif type1 == "Enseignant":
            return render(request, 'dashBoardEnseignant.html',{'user': user})
    else:
        return HttpResponseRedirect("/")

def renderConfiguration(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    if request.method == 'POST':
        parametre_recherche = request.POST.get('anneer')
        search_results = Parametre.objects.filter(anneeSoutenance=parametre_recherche)
        return render(request, 'configuration.html', {'search_results': search_results,'user': user})
    else:
        listeParametre = Parametre.objects.all()  
        return render(request, 'configuration.html', {'listeParametre': listeParametre,'user': user}) 

def ajoutParametre(request):
    dateDebSoutenance=request.POST["dateDebSoutenance"]
    dateFinSoutenace=request.POST["dateFinSoutenace"]
    dureeSoutenance=request.POST["dureeSoutenance"]
    ecartSoutenance=request.POST["ecartSoutenance"]
    anneeSoutenance=request.POST["anneeSoutenance"]
    nbrDomaineEnseignant=request.POST["nbrDomaineEnseignant"]
    nbrMinuteOccupEns=request.POST["nbrMinuteOccupEns"]
    nbrThemeEns=request.POST["nbrThemeEns"]
    nbrDemande=request.POST["nbrDemande"]
    nbrDemandeAccepter=request.POST["nbrDemandeAccepter"]
    dateDebConfigEns=request.POST["dateDebConfigEns"]
    dateFinConfigEns=request.POST["dateFinConfigEns"]
    dateDebDem=request.POST["dateDebDem"]
    dateFinDem=request.POST["dateFinDem"]
    dateDebRep=request.POST["dateDebRep"]
    dateFinRep=request.POST["dateFinRep"]
    dateDebTraitement=request.POST["dateDebTraitement"]
    dateLimiteTtraitement=request.POST["dateLimiteTtraitement"]
    eAdmin=request.session['user_email']
    admin = Administrateur.objects.get(email=eAdmin)
    np=Parametre(dateDebSoutenance=dateDebSoutenance,dateFinSoutenace=dateFinSoutenace,dureeSoutenance=dureeSoutenance,ecartSoutenance=ecartSoutenance,anneeSoutenance=anneeSoutenance,nbrDomaineEnseignant=nbrDomaineEnseignant,nbrMinuteOccupEns=nbrMinuteOccupEns,nbrThemeEns=nbrThemeEns,nbrDemande=nbrDemande,nbrDemandeAccepter=nbrDemandeAccepter,dateDebConfigEns=dateDebConfigEns,dateFinConfigEns=dateFinConfigEns,dateDebDem=dateDebDem,dateFinDem=dateFinDem,dateDebRep=dateDebRep,dateFinRep=dateFinRep,dateDebTraitement=dateDebTraitement,dateLimiteTtraitement=dateLimiteTtraitement,idAdministrateur=admin)
    np.save()
    messages.success(request,"Configuration ajoutée avec succès")
    return HttpResponseRedirect(reverse("configuration"))

def suprimerParametre(request,id):
    psup=Parametre.objects.get(id=id)
    psup.delete()
    messages.success(request,"Configuration supprimée avec succès")
    return HttpResponseRedirect(reverse("configuration"))

def rendermodifierParametre(request,id):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    prech=Parametre.objects.get(id=id)
    setinfo={
        'prechercher':prech,
        'user': user,
    }
    return render(request,'modifierParametre.html',setinfo)

def MAJParametre(request,id):
    newId=request.POST["id"]
    oldp=Parametre.objects.get(id=newId)
    dateDebSoutenance=request.POST["dateDebSoutenance"]
    dateFinSoutenace=request.POST["dateFinSoutenace"]
    dureeSoutenance=request.POST["dureeSoutenance"]
    ecartSoutenance=request.POST["ecartSoutenance"]
    anneeSoutenance=request.POST["anneeSoutenance"]
    nbrDomaineEnseignant=request.POST["nbrDomaineEnseignant"]
    nbrMinuteOccupEns=request.POST["nbrMinuteOccupEns"]
    nbrThemeEns=request.POST["nbrThemeEns"]
    nbrDemande=request.POST["nbrDemande"]
    nbrDemandeAccepter=request.POST["nbrDemandeAccepter"]
    dateDebConfigEns=request.POST["dateDebConfigEns"]
    dateFinConfigEns=request.POST["dateFinConfigEns"]
    dateDebDem=request.POST["dateDebDem"]
    dateFinDem=request.POST["dateFinDem"]
    dateDebRep=request.POST["dateDebRep"]
    dateFinRep=request.POST["dateFinRep"]
    dateDebTraitement=request.POST["dateDebTraitement"]
    dateLimiteTtraitement=request.POST["dateLimiteTtraitement"]
    oldp.dateDebSoutenance=dateDebSoutenance
    oldp.dateFinSoutenace=dateFinSoutenace
    oldp.dureeSoutenance=dureeSoutenance
    oldp.ecartSoutenance=ecartSoutenance
    oldp.anneeSoutenance=anneeSoutenance
    oldp.nbrDomaineEnseignant=nbrDomaineEnseignant
    oldp.nbrMinuteOccupEns=nbrMinuteOccupEns
    oldp.nbrThemeEns=nbrThemeEns
    oldp.nbrDemande=nbrDemande
    oldp.nbrDemandeAccepter=nbrDemandeAccepter
    oldp.dateDebConfigEns=dateDebConfigEns
    oldp.dateFinConfigEns=dateFinConfigEns
    oldp.dateDebDem=dateDebDem
    oldp.dateFinDem=dateFinDem
    oldp.dateDebRep=dateDebRep
    oldp.dateFinRep=dateFinRep
    oldp.dateDebTraitement=dateDebTraitement
    oldp.dateLimiteTtraitement=dateLimiteTtraitement
    oldp.save()
    messages.success(request,"Configuration modifiée avec succès")
    return HttpResponseRedirect(reverse("configuration"))

def renderPlanning(request):
    eUser = request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)

    try:
        salles, parametres, occupations_salles, enseignants = get_data()
        planning = generate_planning(salles, parametres, occupations_salles, enseignants)
    except Exception as e:
        logger.error("Error generating planning: %s", e)
        planning = {}

    planning_hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    context = {
        'user': user,
        'planning': planning,
        'planning_hours': planning_hours,
        'days': days,
    }

    return render(request, 'planning.html', context)




def renderEvaluation(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    eEnseignant=request.session['user_email']
    listeLeader = Leader.objects.filter(idEnseignantEncadrant=eEnseignant)
    return render(request, 'evaluation.html', {'listeLeader': listeLeader,'user': user})

def rendermodifierLeaderR(request,email):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    srech=Leader.objects.get(email=email)
    setinfo={
        'lrechercher':srech,
        'user': user,
    }
    return render(request,'modifierLeader.html',setinfo)

def MAJLeaderR(request,email):
    oldr=Leader.objects.get(email=email)
    r=request.POST["remarque"]
    e=request.POST["etat"]
    oldr.remarque_memoire=r
    oldr.etat_memoire=e
    oldr.save()
    messages.success(request,"Leader modifié avec succès")
    return HttpResponseRedirect(reverse("evaluation"))

def accepter(request, id):
    
    demande_acceptee = Demande.objects.get(id=id)
    demande_acceptee.reponse = "Accepté"
    demande_acceptee.save()
    messages.success(request,"réponse envoyé avec succès")
    autres_demandes = Demande.objects.filter(idTheme=demande_acceptee.idTheme).exclude(id=id)
    for demande in autres_demandes:
        demande.reponse = "Refusé"
        demande.save()

    return HttpResponseRedirect(reverse("demandes"))


# Génération de planning 

logger = logging.getLogger(__name__)

def get_data():
    salles = [{"num_bloc": random.randint(1, 3), "num_salle": random.randint(101, 120)} for _ in range(20)]
    today = datetime.today()
    parametres = {
        "dateDebSoutenance": today + timedelta(days=1),
        "dateFinSoutenance": today + timedelta(days=60),
        "dureeSoutenance": 90,
        "ecartSoutenance": 30,
        "anneeSoutenance": today.year
    }
    occupations_salles = []
    for _ in range(100):
        date_occupation = today + timedelta(days=random.randint(1, 60))
        heure_debut = time(random.randint(8, 15), random.choice([0, 30]))
        duree = timedelta(minutes=parametres["dureeSoutenance"])
        heure_fin = (datetime.combine(datetime.today(), heure_debut) + duree).time()
        occupations_salles.append({
            "date_occupation": date_occupation,
            "heure_debut": heure_debut,
            "heure_fin": heure_fin,
            "num_bloc": random.randint(1, 3),
            "num_salle": random.randint(101, 120)
        })
    enseignants = []
    for i in range(30):
        enseignants.append({
            "email": f"enseignant{i + 1}@example.com",
            "occupations": [],
            "indispos": generate_teacher_unavailabilities(today, parametres["dateFinSoutenance"])
        })
    return salles, parametres, occupations_salles, enseignants

def generate_teacher_unavailabilities(start_date, end_date):
    indispos = []
    current_date = start_date
    while current_date <= end_date:
        if random.random() < 0.2:
            indispos.append({
                "date": current_date,
                "heure_debut": time(8, 0),
                "heure_fin": time(18, 0)
            })
        else:
            if random.random() < 0.5:
                heure_debut = time(random.randint(8, 15), random.choice([0, 30]))
                duree = timedelta(minutes=random.choice([90, 120, 180]))
                heure_fin = (datetime.combine(datetime.today(), heure_debut) + duree).time()
                indispos.append({
                    "date": current_date,
                    "heure_debut": heure_debut,
                    "heure_fin": heure_fin
                })
        current_date += timedelta(days=1)
    return indispos

def generate_creneaux(heure_debut, heure_fin, duree_soutenance, ecart_soutenance):
    creneaux = []
    current_time = datetime.combine(datetime.today(), heure_debut)
    end_time = datetime.combine(datetime.today(), heure_fin)
    duree_soutenance_delta = timedelta(minutes=duree_soutenance)
    ecart_soutenance_delta = timedelta(minutes=ecart_soutenance)
    while current_time + duree_soutenance_delta <= end_time:
        creneaux.append({
            "heureD": current_time.time(),
            "heureF": (current_time + duree_soutenance_delta).time()
        })
        current_time += duree_soutenance_delta + ecart_soutenance_delta
    return creneaux

def is_salle_disponible(date, heureD, heureF, occupations_salles, num_bloc, num_salle):
    for occupation in occupations_salles:
        if (occupation["date_occupation"].date() == date.date() and
            occupation["num_bloc"] == num_bloc and
            occupation["num_salle"] == num_salle and
            not (heureF <= occupation["heure_debut"] or heureD >= occupation["heure_fin"])):
            return False
    return True

def is_enseignant_disponible(email, jour, heureD, heureF, enseignants):
    for enseignant in enseignants:
        if enseignant["email"] == email:
            for occupation in enseignant["occupations"]:
                if not (heureF <= occupation["heure_debut"] or heureD >= occupation["heure_fin"]):
                    return False
            for indispo in enseignant["indispos"]:
                if (indispo["date"].date() == jour and
                    not (heureF <= indispo["heure_debut"] or heureD >= indispo["heure_fin"])):
                    return False
    return True

def assign_occupations(jury, current_date, creneau):
    for enseignant in jury:
        enseignant["occupations"].append({
            "date": current_date,
            "heure_debut": creneau["heureD"],
            "heure_fin": creneau["heureF"]
        })

def generate_planning(salles, parametres, occupations_salles, enseignants):
    planning = defaultdict(lambda: defaultdict(list))
    start_date = parametres["dateDebSoutenance"]
    end_date = parametres["dateFinSoutenance"]
    duree_soutenance = parametres["dureeSoutenance"]
    ecart_soutenance = parametres["ecartSoutenance"]
    jour_debut = time(8, 0)
    jour_fin = time(18, 0)
    current_date = start_date
    while current_date <= end_date:
        jour_semaine = current_date.strftime("%A")
        creneaux = generate_creneaux(jour_debut, jour_fin, duree_soutenance, ecart_soutenance)
        for creneau in creneaux:
            for salle in salles:
                if not is_salle_disponible(current_date, creneau["heureD"], creneau["heureF"], occupations_salles, salle["num_bloc"], salle["num_salle"]):
                    continue
                jury = random.sample(enseignants, 5)
                if all(is_enseignant_disponible(enseignant["email"], current_date, creneau["heureD"], creneau["heureF"], enseignants) for enseignant in jury):
                    assign_occupations(jury, current_date, creneau)
                    creneau_info = {
                        "heure_debut": creneau["heureD"].strftime("%H:%M"),
                        "heure_fin": creneau["heureF"].strftime("%H:%M"),
                        "salle": f"{salle['num_bloc']}-{salle['num_salle']}",
                        "enseignants": [enseignant["email"] for enseignant in jury],
                        "leader_groupe": "leader@example.com"
                    }
                    planning[jour_semaine][creneau["heureD"].strftime("%H:%M")].append(creneau_info)
        current_date += timedelta(days=1)
    return planning


# Explanation:
# Rooms: We now generate 20 rooms to ensure a sufficient number of venues for the soutenances.

# Extended Date Range: The period for soutenances has been extended to 60 days, allowing for more scheduling opportunities.

# Room Occupations: A total of 100 room occupations are generated dynamically, representing a more realistic and varied schedule.

# Teachers: The number of teachers has been increased to 30, with dynamic unavailabilities ensuring realistic constraints in scheduling.

# Teacher Unavailabilities: Teachers' unavailabilities are generated to reflect different patterns, including full-day unavailabilities and partial-day periods.

# This comprehensive approach will ensure that the planning schedule is well-populated with multiple soutenances occurring daily, adhering to real-world constraints and requirements.


# Générer PDF
from bs4 import BeautifulSoup 
def generate_pdf(request):
    eUser = request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)

    try:
        salles, parametres, occupations_salles, enseignants = get_data()
        planning = generate_planning(salles, parametres, occupations_salles, enseignants)
    except Exception as e:
        logger.error("Error generating planning: %s", e)
        planning = {}

    planning_hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    context = {
        'user': user,
        'planning': planning,
        'planning_hours': planning_hours,
        'days': days,
    }

    html_string = render_to_string('planning.html', context)

    # Utilisation de BeautifulSoup pour extraire la section désirée du HTML
    soup = BeautifulSoup(html_string, 'html.parser')
    table_section = soup.select_one('.container-fluid.pt-4.px-4 .bg-secondary.text-center.rounded.p-4')

    if table_section:
        form = table_section.find('form')
        if form:
            form.decompose()

        # Inclure les styles CSS dans la section head pour le PDF
        pdf_css = '''
        <style>
            body {
                font-size: 12px;
            }
            .custom-table {
                width: 100%;
                border-collapse: collapse;
                margin: 0 auto;
            }
            .custom-table th, .custom-table td {
                border: 1px solid black;
                padding: 5px;
                text-align: left;
                font-size: 10px;
                word-wrap: break-word; /* Ensure long words break to avoid overflow */
                /*height: 100px; /* Increase cell height */
            }
            .custom-table th {
                background-color: #f2f2f2;
            }
            .custom-table td {
                vertical-align: top;
            }
            .soutenance-item {
                padding: 2px;
                margin-bottom: 2px; /* Space between items */
            }
            .available-slot {
                background-color: #d4edda;
            }
            .unavailable-slot {
                background-color: #f8d7da;
            }
            .available-slot p, .unavailable-slot p {
                margin: 0;
                padding: 0;
            }
        </style>
        '''

        table_section.insert_before(BeautifulSoup(pdf_css, 'html.parser'))

        html_table_string = f"<html><head>{pdf_css}</head><body>{str(table_section)}</body></html>"
    else:
        logger.error("No planning table section found in the HTML")
        html_table_string = "<p>No planning table available</p>"

    no_margin_css = CSS(string='''
        @page { margin: 10px; }
        body { margin: 0; }
    ''')

    html = HTML(string=html_table_string)
    pdf_file = html.write_pdf(stylesheets=[no_margin_css])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="planning.pdf"'

    return response
# def generate_pdf(request):   2 
#     eUser = request.session['user_email']
#     user = Utilisateur.objects.get(email=eUser)

#     try:
#         salles, parametres, occupations_salles, enseignants = get_data()
#         planning = generate_planning(salles, parametres, occupations_salles, enseignants)
#     except Exception as e:
#         logger.error("Error generating planning: %s", e)
#         planning = {}

#     planning_hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

#     context = {
#         'user': user,
#         'planning': planning,
#         'planning_hours': planning_hours,
#         'days': days,
#     }

#     html_string = render_to_string('planning.html', context)

#     # Utilisation de BeautifulSoup pour extraire la section désirée du HTML
#     soup = BeautifulSoup(html_string, 'html.parser')
#     table_section = soup.select_one('.container-fluid.pt-4.px-4 .bg-secondary.text-center.rounded.p-4')

#     if table_section:
#         form = table_section.find('form')
#         if form:
#             form.decompose()

#         # Inclure les styles CSS dans la section head
#         head_content = '''
#         <style>
#             body {
#                 font-size: 12px;
#             }
#             .custom-table {
#                 width: 100%;
#                 border-collapse: collapse;
#                 margin: 0 auto;
#             }
#             .custom-table th, .custom-table td {
#                 border: 1px solid black;
#                 padding: 2px;
#                 text-align: left;
#                 font-size: 10px;
#             }
#             .custom-table th {
#                 background-color: #f2f2f2;
#             }
#             .custom-table td {
#                 vertical-align: top;
#             }
#             .soutenance-item:not(:first-of-type) {
#                 border-top: 1px solid black;
#             }
#             .soutenance-item {
#                 padding: 0px;
#             }
#             .available-slot {
#                 background-color: #d4edda;
#                 display: flex;
#                 align-items: center;
#             }
#             .unavailable-slot {
#                 background-color: #f8d7da;
#                 display: flex;
#                 align-items: center;
#             }
#         </style>
#         '''

#         # Insertion du contenu du head et du CSS dans la section table
#         table_section.insert_before(BeautifulSoup(head_content, 'html.parser'))

#         html_table_string = f"<html><head>{head_content}</head><body>{str(table_section)}</body></html>"
#     else:
#         logger.error("No planning table section found in the HTML")
#         html_table_string = "<p>No planning table available</p>"

#     html = HTML(string=html_table_string)
#     pdf_file = html.write_pdf(stylesheets=[])

#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="planning.pdf"'

#     return response
    
# def generate_pdf(request):   1
#     eUser = request.session['user_email']
#     user = Utilisateur.objects.get(email=eUser)

#     try:
#         salles, parametres, occupations_salles, enseignants = get_data()
#         planning = generate_planning(salles, parametres, occupations_salles, enseignants)
#     except Exception as e:
#         logger.error("Error generating planning: %s", e)
#         planning = {}

#     planning_hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

#     context = {
#         'user': user,
#         'planning': planning,
#         'planning_hours': planning_hours,
#         'days': days,
#     }

#     html_string = render_to_string('planning.html', context)

#     # Utilisation de BeautifulSoup pour extraire la section désirée du HTML
#     soup = BeautifulSoup(html_string, 'html.parser')
#     table_section = soup.select_one('.container-fluid.pt-4.px-4 .bg-secondary.text-center.rounded.p-4')

#     if table_section:
#         form = table_section.find('form')
#         if form:
#             form.decompose()

#         head_content = '''
#         <style>
#             .custom-table {
#                 width: 100%;
#                 border-collapse: collapse;
#             }
#             .custom-table th, .custom-table td {
#                 border: 1px solid black;
#                 padding: 1px;
#                 text-align: left;
#             }
#             .custom-table th {
#                 background-color: #f2f2f2;
#             }
#             .custom-table td {
#                 height: 10px;
#                 vertical-align: top;
#             }
#         </style>
#         '''

#         # Insertion du contenu du head et du CSS dans la section table
#         table_section.insert_before(BeautifulSoup(head_content, 'html.parser'))

#         html_table_string = f"<html><head>{head_content}</head><body>{str(table_section)}</body></html>"
#     else:
#         logger.error("No planning table section found in the HTML")
#         html_table_string = "<p>No planning table available</p>"

#     html = HTML(string=html_table_string)
#     pdf_file = html.write_pdf()

#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="planning.pdf"'

#     return response


