from django.shortcuts import render
from soutenanceApp.models import Utilisateur,Administrateur,Salle,Occupation_salle,Enseignant,Occupation_Enseignant,Domain_expertise,Theme,Leader,Demande,Evaluation,EnseignantDomaineExpertise,Parametre
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    return HttpResponseRedirect(reverse("salles"))

def suprimerSalle(request,id):
    ssup=Salle.objects.get(id=id)
    ssup.delete()
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
    return HttpResponseRedirect(reverse("occupationSalle", args=[id]))

def suprimerOccupationSalle(request,id,ids):
    sosup=Occupation_salle.objects.get(ids=ids)
    sosup.delete()
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
    return HttpResponseRedirect(reverse("domaineAdmin"))

def suprimerDomaineAdmin(request,id):
    dasup=Domain_expertise.objects.get(id=id)
    dasup.delete()
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
    return HttpResponseRedirect(reverse("occupationEnseignant"))

def suprimerOccupationEnseignant(request,ide):
    soesup=Occupation_Enseignant.objects.get(ide=ide)
    soesup.delete()
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
    return HttpResponseRedirect(reverse("domaineEnseignant"))

def suprimerDomaineEnseignant(request,id):
    desup=EnseignantDomaineExpertise.objects.get(id=id)
    desup.delete()
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
    return HttpResponseRedirect(reverse("themes"))

def suprimerTheme(request,id):
    tsup=Theme.objects.get(id=id)
    tsup.delete()
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
    return HttpResponseRedirect(reverse("configuration"))

def suprimerParametre(request,id):
    psup=Parametre.objects.get(id=id)
    psup.delete()
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
    return HttpResponseRedirect(reverse("configuration"))

def renderPlanning(request):
    eUser=request.session['user_email']
    user = Utilisateur.objects.get(email=eUser)
    return render(request,'planning.html',{'user': user})

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
    return HttpResponseRedirect(reverse("evaluation"))

def accepter(request, id):
    demande_acceptee = Demande.objects.get(id=id)
    demande_acceptee.reponse = "Accepté"
    demande_acceptee.save()
    autres_demandes = Demande.objects.filter(idTheme=demande_acceptee.idTheme).exclude(id=id)
    for demande in autres_demandes:
        demande.reponse = "Refusé"
        demande.save()
    return HttpResponseRedirect(reverse("demandes"))
