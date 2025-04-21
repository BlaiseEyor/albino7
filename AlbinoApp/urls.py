from django.urls import path # type: ignore
from AlbinoApp.views import(
    index,
    lireplus,
    actualite,
    contact,
    login,
    deconnexion,
    )

urlpatterns = [
    path('', index, name='index'),
    path('lire_plus/', lireplus, name='lire_plus'),
    path('actualite/', actualite, name='actualite'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('deconnexion/', deconnexion, name='deconnexion'),
]