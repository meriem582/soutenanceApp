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
import locale



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
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from collections import defaultdict
import random
import datetime
import logging

logger = logging.getLogger(__name__)

def renderPlanning(request):
    eUser = request.session.get('user_email')
    user = Utilisateur.objects.get(email=eUser)

    try:
        # Récupération des données
        salles, occupations_salles, enseignants, leaders = get_data()

        # Logging des données récupérées
        logger.debug(f"Salles: {salles}")
        logger.debug(f"Occupations salles: {occupations_salles}")
        logger.debug(f"Enseignants: {enseignants}")
        logger.debug(f"Leaders: {leaders}")

        # Utilisation de valeurs statiques prédéfinies
        start_date = datetime.date(2024, 6, 25)
        end_date = datetime.date(2024, 7, 2)
        days = [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
        planning_hours = [f"{hour:02d}:00" for hour in range(9, 17)]
        
        # Génération du planning
        planning = generate_planning(salles, occupations_salles, enseignants, leaders, days, planning_hours)

        # Logging des données passées au template
        logger.debug(f"Planning: {dict(planning)}")
        logger.debug(f"Days: {days}")
        logger.debug(f"Planning hours: {planning_hours}")

        # Rendu de la vue avec les données
        return render(request, 'planning.html', {
            'user': user,
            'planning': dict(planning),
            'days': days,
            'planning_hours': planning_hours,
        })

    except Exception as e:
        logger.error(f"Error generating planning: {e}", exc_info=True)
        return render(request, 'planning.html', {
            'user': user,
            'planning': {},
            'days': [],
            'planning_hours': [],
            'error': 'Erreur lors de la génération du planning'
        })

def get_data():
    salles = list(Salle.objects.values('num_bloc', 'num_salle'))
    occupations_salles = list(Occupation_salle.objects.values('date_occupation', 'heure_debut', 'heure_fin', 'idSalle__num_bloc', 'idSalle__num_salle'))
    enseignants = list(Enseignant.objects.values('email'))

    teacher_unavailabilities = {}
    for enseignant in enseignants:
        email = enseignant['email']
        occupations = Occupation_Enseignant.objects.filter(idEnseignant__email=email).values('date_occupation', 'heure_debut', 'heure_fin')
        indispos = [{
            "date": occupation['date_occupation'],
            "heure_debut": occupation['heure_debut'],
            "heure_fin": occupation['heure_fin']
        } for occupation in occupations]
        teacher_unavailabilities[email] = indispos

    for enseignant in enseignants:
        email = enseignant['email']
        enseignant['indispos'] = teacher_unavailabilities.get(email, [])

    leaders = list(Leader.objects.values('email', 'nom_binom', 'prenom_binom', 'annee_etude', 'domain', 'idTheme__intitule', 'idEnseignantEncadrant__email'))

    return salles, occupations_salles, enseignants, leaders

def generate_planning(salles, occupations_salles, enseignants, leaders, days, planning_hours):
    planning = defaultdict(lambda: defaultdict(list))
    used_leaders = set()
    total_leaders = len(leaders)

    for day in days:
        for hour in planning_hours:
            for salle in salles:
                if not is_salle_disponible(day, hour, occupations_salles, salle["num_bloc"], salle["num_salle"]):
                    continue

                jury = random.sample(enseignants, 5)
                enseignants_disponibles = all(is_enseignant_disponible(enseignant["email"], day, hour, enseignants) for enseignant in jury)

                if enseignants_disponibles:
                    available_leaders = [leader for leader in leaders if leader['email'] not in used_leaders]
                    if not available_leaders:
                        logger.info("Tous les leaders ont été utilisés")
                        break

                    leader = random.choice(available_leaders)
                    used_leaders.add(leader['email'])

                    soutenance_info = {
                        "salle": f"{salle['num_bloc']}-{salle['num_salle']}",
                        "leader_groupe": leader['email'],
                        "enseignants": [enseignant['email'] for enseignant in jury]
                    }
                    planning[day][hour].append(soutenance_info)
                    logger.debug(f"Added soutenance: {soutenance_info} on {day} at {hour}")

                    if len(used_leaders) >= total_leaders:
                        logger.info("Limite des leaders atteinte")
                        break
            if len(used_leaders) >= total_leaders:
                break
        if len(used_leaders) >= total_leaders:
            break

    logger.debug("Final planning structure:")
    for day, hours in planning.items():
        for hour, soutenances in hours.items():
            logger.debug(f"Day: {day}, Hour: {hour}, Soutenances: {soutenances}")

    logger.info("Planning generation completed")
    return planning

def is_salle_disponible(day, hour, occupations_salles, num_bloc, num_salle):
    for occupation in occupations_salles:
        if (
            occupation['date_occupation'].strftime('%Y-%m-%d') == day and
            occupation['heure_debut'].strftime('%H:%M') <= hour <= occupation['heure_fin'].strftime('%H:%M') and
            occupation['idSalle__num_bloc'] == num_bloc and
            occupation['idSalle__num_salle'] == num_salle
        ):
            logger.debug(f"Salle {num_bloc}-{num_salle} non disponible pour le créneau {hour} le {day}")
            return False
    return True

def is_enseignant_disponible(email, day, hour, enseignants):
    for enseignant in enseignants:
        if enseignant['email'] == email:
            for indispo in enseignant['indispos']:
                if (
                    indispo['date'].strftime('%Y-%m-%d') == day and
                    indispo['heure_debut'].strftime('%H:%M') <= hour <= indispo['heure_fin'].strftime('%H:%M')
                ):
                    logger.debug(f"Enseignant {email} non disponible pour le créneau {hour} le {day}")
                    return False
    return True









def generate_pdf(request):
    eUser = request.session.get('user_email')
    user = Utilisateur.objects.get(email=eUser)

    try:
        # Récupérer les données nécessaires pour le planning
        salles, occupations_salles, enseignants, leaders = get_data()

        # Utiliser les mêmes valeurs que pour la génération du planning HTML
        start_date = datetime.date(2024, 6, 25)
        end_date = datetime.date(2024, 7, 2)
        days = [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
        planning_hours = [f"{hour:02d}:00" for hour in range(9, 17)]
        
        planning = generate_planning(salles, occupations_salles, enseignants, leaders, days, planning_hours)
        
        # Préparer le contexte pour le rendu HTML
        context = {
            'user': user,
            'planning': dict(planning),
            'days': days,
            'planning_hours': planning_hours,
        }
        
        # Rendre le contenu HTML du planning
        html_string = render_to_string('planning.html', context)
        soup = BeautifulSoup(html_string, 'html.parser')
        table_section = soup.find('table')
        
        if table_section:
            # Style CSS pour le PDF
            pdf_css = '''
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                    font-size: 10px;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
                    vertical-align: top;
                    word-wrap: break-word;
                }
                th {
                    background-color: #f2f2f2;
                }
                @page {
                    size: A4 landscape;
                    margin: 1cm;
                }
            </style>
            '''
            html_content = f'<html><head>{pdf_css}</head><body>{str(table_section)}</body></html>'
            
            # Générer le PDF
            pdf_file = HTML(string=html_content).write_pdf(stylesheets=[CSS(string=pdf_css)])
            
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="planning.pdf"'
            return response
        else:
            return HttpResponse("Table section not found in the HTML content.")
    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return HttpResponse("Error generating PDF.")
