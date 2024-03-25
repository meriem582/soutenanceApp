from django.urls import path
from soutenanceApp import views
# de views c'est la fonctions ,
urlpatterns=[
    path('',views.renderIndex,name="index"),
    path('dashBoardAdmin/',views.renderDashBoardAdmin,name="dashBoardAdmin"),
    path('dashBoardEnseignant/',views.renderDashBoardEnseignantt,name="dashBoardEnseignant"),
    path('dashBoardLeader/',views.renderDashBoardLeader,name="dashBoardLeader"),
    path('utilisateur/',views.renderUtilisateur,name="utilisateur"),
    path('salles/',views.renderSalles,name="salles"),
    path('configuration/',views.renderConfiguration,name="configuration"),
    path('planning/',views.renderPlanning,name="planning"),
    path('themes/',views.renderThemes,name="themes"),
    path('infoPersonnel/',views.renderInfoPersonnel,name="infoPersonnel"),
    path('demandes/',views.renderDemandes,name="demandes"),
    path('evaluation/',views.renderEvaluation,name="evaluation"),
    path('demanderthemes/',views.renderDemanderThemes,name="demanderthemes"),
    path('deposerMemoire/',views.renderDeposerMemoire,name="deposerMemoire"),
]