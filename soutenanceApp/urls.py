from django.urls import path
from soutenanceApp import views
# de views c'est la fonctions ,
urlpatterns=[
    path('',views.renderIndex),
    path('dashBoardAdmin/',views.renderDashBoardAdmin,name="dashBoardAdmin"),
    path('dashBoardEnseignant/',views.renderDashBoardEnseignantt,name="dashBoardEnseignant"),
    path('dashBoardLeader/',views.renderDashBoardLeader,name="dashBoardLeader"),
]