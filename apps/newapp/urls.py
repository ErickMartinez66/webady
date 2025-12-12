from django.urls import path
from . import views



urlpatterns = [
      path('principal/', views.vistaprin,name="principal"),
      path('principal/perfumes/', views.vistaperfumes, name="perfumes"),
      path('principal/desodorantes/', views.vistadesodo, name="desodorantes"),
      path('principal/cremas/', views.vistacremas, name="cremas"),
      
]


