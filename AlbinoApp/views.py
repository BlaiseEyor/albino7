from django.contrib import messages
import re
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse # type: ignore
from AlbinoApp.models import Contact
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from Dashadmin.models import Add_admin, Add_mission, Add_pubfb
from django.utils.timezone import now, timedelta
from django.contrib.auth import logout
from datetime import datetime

# Create your views here.

def index(request): 
    # Calculer la date et l'heure des dernières 24 heures
    dernieres_96h = now() - timedelta(hours=96) 
    # Récupérer les missions
    missions = Add_mission.objects.filter(date__gte=dernieres_96h).order_by('-date')
    return render(request, 'AlbinoApp/index.html', {'missions': missions})

def lireplus(request):
    return render(request, 'AlbinoApp/lire_plus.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return JsonResponse({"error_message": "L'email et le mot de passe sont obligatoires!"})

        try:
            user = Add_admin.objects.get(email=email)  # Vérifie si l'utilisateur existe
        except Add_admin.DoesNotExist:
            return JsonResponse({"error_message": "Aucun compte trouvé avec cet email!"})

        if check_password(password, user.password):  # Vérifie si le mot de passe correspond
            request.session['user_id'] = user.id  # Stocke l'ID de l'utilisateur dans la session
            request.session["just_logged_in"] = True
            return JsonResponse({'success': True, 'message' : "Connexion réussie, redirection en cours...", 'redirect': reverse('accueil')})
        else:
            return JsonResponse({"error_message": "Le mot de passe que vous avez entrer est incorrect!"})
    return render(request, 'AlbinoApp/login.html')

def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        
        if not all([nom, email, sujet, message]):
            return JsonResponse({'error_message': "Tous les champs sont obligatoires!"})

        email_valide = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(email_valide, email):
            return JsonResponse({'error_message': "L'adresse e-mail que vous avez saisie n'est pas valide!"})
        
        if Contact.objects.filter(email=email).exists():
            return JsonResponse({'error_message': "Cet email existe déjà."})
            
        contact = Contact(
            nom=nom, 
            email=email, 
            sujet=sujet, 
            message=message, 
            )
        contact.save()
        
        message_success = {
            "success" : True,
            "message" : "Votre message a été bien envoyé. Merci pour votre confiance!"
        }
        return JsonResponse(message_success)
    return render(request, 'AlbinoApp/contact.html')

def actualite(request):
    # Initialisation des variables pour les missions
    missions_recentes = []
    missions_anciennes = []
    missions_archivees = []
    date_str = request.GET.get('date')  # Date envoyée dans la requête GET

    # Calcul des seuils de temps pour les catégories
    maintenant = datetime.now()
    dans_96h = maintenant - timedelta(hours=96)
    dans_120h = maintenant - timedelta(hours=120)
    dans_1_semaine = maintenant - timedelta(weeks=1)

    # Si une date est spécifiée dans la recherche
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            all_missions = Add_mission.objects.filter(date__date=date_obj)

            if all_missions.exists():
                messages.success(request, f"{all_missions.count()} mission(s) trouvée(s) pour le {date_str}.")
            else:
                messages.error(request, f"Aucune mission trouvée pour le {date_str}.")

            # Pas de filtre supplémentaire ici
            missions_recentes = all_missions
            missions_anciennes = []
            missions_archivees = []

        except ValueError:
            messages.error(request, "Format de date invalide. Veuillez sélectionner une date correcte.")
    else:
        # Si aucune date n'est donnée, afficher toutes les missions
        all_missions = Add_mission.objects.all()

        missions_recentes = all_missions.filter(date__gte=dans_96h).order_by('-date')
        missions_anciennes = all_missions.filter(date__lt=dans_120h, date__gte=dans_1_semaine).order_by('-date')
        missions_archivees = all_missions.filter(date__lt=dans_1_semaine).order_by('-date')[:6]

    # Retourner toutes les missions et les messages
    return render(request, 'AlbinoApp/actualite.html', {
        'missions_recentes': missions_recentes,
        'missions_anciennes': missions_anciennes,
        'missions_archivees': missions_archivees,
        'date_str': date_str  # Pour conserver la date dans le formulaire
    })

def deconnexion(request):
    logout(request)
    return redirect('login')
