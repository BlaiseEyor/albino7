from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings  
import datetime

class CustomSessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Récupérer le temps de la dernière activité
        last_activity = request.session.get('last_activity')
        current_time = datetime.datetime.now().timestamp()

        if last_activity:
            # Si le temps écoulé dépasse SESSION_EXPIRE_SECONDS
            if current_time - last_activity > settings.SESSION_EXPIRE_SECONDS:
                # Détruire la session et rediriger vers la page de connexion
                request.session.flush()
                return redirect('login')  # 'login' est le nom de votre vue de connexion

        # Mettre à jour le temps de la dernière activité
        request.session['last_activity'] = current_time
