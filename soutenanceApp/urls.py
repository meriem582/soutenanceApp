from django.urls import path
from soutenanceApp import views
# de views c'est la fonctions ,
urlpatterns=[
    path('',views.renderIndex),
    path('dashBoard/',views.renderDashBoard,name="dashBoard"),
]