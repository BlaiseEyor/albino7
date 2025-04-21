from django.urls import path
from django.conf.urls.static import static 
from Albino import settings


from Dashadmin.views import (
    accueil,
    pub_mission,
    pub_annonce_FB,
    liste_avis,
    ajouter_admin,
    supprimer_pub,
    modifier_mission
    )

urlpatterns = [
    path('accueil', accueil, name='accueil'),
    path('pub_mission/', pub_mission, name='pub_mission'),
    path('pub_annonce_FB/', pub_annonce_FB, name='pub_annonce_FB'),
    path('liste_avis/', liste_avis, name='liste_avis'),
    path('ajouter_admin/', ajouter_admin, name='ajouter_admin'),
    path('supprimer_pub/<int:publication_id>/', supprimer_pub, name='supprimer_pub'),
    path('modifier_mission/', modifier_mission, name='modifier_mission'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ajouter les handlers d'erreurs en dehors de urlpatterns
handler403 = 'Dashadmin.views.custom_permission_denied_view'