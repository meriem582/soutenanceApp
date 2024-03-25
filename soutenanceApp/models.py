from django.db import models

# Create your models here.
class Utilisateur(models.Model):
    email=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(max_length=50)
    type_User=models.CharField(max_length=50)
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    


class Meta:
    db_table="utilisateur"



class Administrateur(models.Model):
    email=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,primary_key=True)


class Meta:
    db_table="administrateur"



class Salle(models.Model):
    num_bloc=models.IntegerField()
    num_salle=models.IntegerField()
    idAdministrateur=models.ForeignKey(Administrateur,on_delete=models.CASCADE)

class Meta:
    unique_together=('num_bloc', 'num_salle')

class Meta:
    db_table="salle"


class Occupation_salle(models.Model):
    date_occupation=models.DateField()
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    idSalle=models.ForeignKey(Salle,on_delete=models.CASCADE)
    idAdministrateur=models.ForeignKey(Administrateur,on_delete=models.CASCADE)

class Meta:
    db_table="occupation_salle"



class Enseignant(models.Model):
    email=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,primary_key=True)
    grade=models.CharField(max_length=50)

class Meta:
    db_table="enseignant"


class Occupation_Enseignant(models.Model):
    date_occupation=models.DateField()
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)

class Meta:
    db_table="occupation_enseignant"



class Domain_expertise(models.Model):
    intitule=models.CharField(max_length=50)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)

class Meta:
    db_table="domaine_expertise"
     



class Theme(models.Model):
    intitule=models.CharField(max_length=50,unique=True)
    domaine=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)

class Meta:
    db_table="theme"

class Leader(models.Model):
    email=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,primary_key=True)
    nom_binom=models.CharField(max_length=50)
    prenom_binom=models.CharField(max_length=50)
    annee_etude=models.CharField(max_length=50)
    memoire=models.BinaryField()
    domain=models.CharField(max_length=50)
    etat_memoire=models.CharField(max_length=50)
    remarque_memoire=models.CharField(max_length=255)
    idEnseignantEncadrant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    idTheme=models.OneToOneField(Theme,on_delete=models.CASCADE)


class Meta:
    db_table="leader"



class Demande(models.Model):
    theme=models.CharField(max_length=50)
    reponse=models.CharField(max_length=50)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    idLeader=models.ForeignKey(Leader,on_delete=models.CASCADE)

class Meta:
    db_table="demande"


class Evaluation(models.Model):
    date_evaluation=models.DateField()
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    role_enseignant=models.CharField(max_length=50)
    idTheme=models.ForeignKey(Theme,on_delete=models.CASCADE)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    idSalle=models.ForeignKey(Salle,on_delete=models.CASCADE)




class Meta:
    db_table="evaluation"
