


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
    email = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)


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
    ids = models.AutoField(primary_key=True)
    date_occupation=models.DateField()
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    idSalle=models.ForeignKey(Salle,on_delete=models.CASCADE)
    idAdministrateur=models.ForeignKey(Administrateur,on_delete=models.CASCADE)

class Meta:
    db_table="occupation_salle"

class Enseignant(models.Model):
    email = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    grade=models.CharField(max_length=50)

class Meta:
    db_table="enseignant"

class Occupation_Enseignant(models.Model):
    ide = models.AutoField(primary_key=True)
    date_occupation=models.DateField()
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)

class Meta:
    db_table="occupation_enseignant"

class Domain_expertise(models.Model):
    intitule=models.CharField(max_length=50)
    idAdministrateur=models.ForeignKey(Administrateur,on_delete=models.CASCADE)

class Meta:
    db_table="domaine_expertise"

class EnseignantDomaineExpertise(models.Model):
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    idDomaineExpertise=models.ForeignKey(Domain_expertise,on_delete=models.CASCADE)
    
class Meta:
    db_table="EnseignantDomaineExpertise"

class Theme(models.Model):
    intitule=models.CharField(max_length=50,unique=True)
    domaine=models.CharField(max_length=50)
    description=models.CharField(max_length=1500)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)

class Meta:
    db_table="theme"

class Leader(models.Model):
    email = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    nom_binom=models.CharField(max_length=50)
    prenom_binom=models.CharField(max_length=50)
    annee_etude=models.CharField(max_length=50)
    memoire=models.BinaryField()
    domain=models.CharField(max_length=50)
    etat_memoire=models.CharField(max_length=50)
    remarque_memoire=models.CharField(max_length=255)
    idEnseignantEncadrant=models.ForeignKey(Enseignant,on_delete=models.CASCADE,null=True)
    idTheme=models.OneToOneField(Theme,on_delete=models.CASCADE,null=True)

class Meta:
    db_table="leader"

class Demande(models.Model):
    idTheme=models.ForeignKey(Theme,on_delete=models.CASCADE)
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
    idLeader=models.ForeignKey(Leader,on_delete=models.CASCADE)
    idEnseignant=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    idSalle=models.ForeignKey(Salle,on_delete=models.CASCADE)

class Meta:
    db_table="evaluation"
