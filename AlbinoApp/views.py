import re
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse # type: ignore
from AlbinoApp.models import Contact
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from Dashadmin.models import Add_admin, Add_mission, Add_pubfb
from django.utils.timezone import now, timedelta
from django.contrib.auth import logout

# Create your views here.

def index(request): 
    # Calculer la date et l'heure des dernières 24 heures
    dernieres_24h = now() - timedelta(hours=24) 
    # Récupérer les missions
    missions = Add_mission.objects.filter(date__gte=dernieres_24h).order_by('-date')
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
    # Calculer les dates de seuil
    dernieres_24h = now() - timedelta(hours=24)
    une_semaine = now() - timedelta(weeks=1)

    # Récupérer les paramètres du formulaire de recherche
    theme = request.GET.get('theme', '')
    date_filtre = request.GET.get('date', '')

    # Initialiser la requête de base
    missions = Add_mission.objects.all()

    # Filtrer par thème si un thème est spécifié
    if theme:
        missions = missions.filter(theme__icontains=theme)

    # Filtrer par date si une date est spécifiée
    if date_filtre == '24h':
        missions = missions.filter(date__gte=dernieres_24h)
    elif date_filtre == 'semaine':
        missions = missions.filter(date__lt=dernieres_24h, date__gte=une_semaine)
    elif date_filtre == 'archive':
        missions = missions.filter(date__lt=une_semaine)

    # Limiter les résultats à 6 par catégorie (tu peux ajuster le nombre)
    missions_recentes = missions.filter(date__gte=dernieres_24h).order_by('-date')[:6]
    missions_anciennes = missions.filter(date__lt=dernieres_24h, date__gte=une_semaine).order_by('-date')[:6]
    missions_archivees = missions.filter(date__lt=une_semaine).order_by('-date')[:6]

    return render(request, 'AlbinoApp/actualite.html', {
        'missions_recentes': missions_recentes,
        'missions_anciennes': missions_anciennes,
        'missions_archivees': missions_archivees,
        'theme': theme,
        'date_filtre': date_filtre,
    })

def deconnexion(request):
    logout(request)
    return redirect('login')
