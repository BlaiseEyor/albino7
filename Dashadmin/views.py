from django.core.cache import cache
from django.contrib import messages
import re
from django.shortcuts import redirect, render 
from django.http import JsonResponse 
from Dashadmin.models import Add_admin, Add_mission, Add_pubfb 
from AlbinoApp.models import Contact 
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


# Create your views here.
def custom_permission_denied_view(request, exception=None):
    return render(request, 'Dashadmin/errors/error_403.html', status=403)

from django.core.cache import cache

def accueil(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = Add_admin.objects.get(pk=user_id)
        except Add_admin.DoesNotExist:
            pass

    if not user:
        messages.error(request, "Veuillez vous connecter pour accéder à cette page")
        return custom_permission_denied_view(request)

    # Compteur visiteurs (unique par session)
    if not request.session.get("counted", False):
        count = cache.get("visitor_count", 0) + 1
        cache.set("visitor_count", count)
        request.session["counted"] = True
    else:
        count = cache.get("visitor_count", 0)

    total_avis = Contact.objects.count()
    total_pub = Add_mission.objects.count()

    context = {
        'user': user,
        'visitor_count': count, 
        'total_avis': total_avis,
        'total_pub': total_pub,
    }

    return render(request, 'Dashadmin/accueil.html', context)

def ajouter_admin(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = Add_admin.objects.get(pk=user_id) 
        except Add_admin.DoesNotExist:
            pass 
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        img = request.FILES.get('img')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        
        if not all([nom, prenom, email, password, c_password]):
            return JsonResponse({'error_message': "Seul le champ image n'est pas obligatoire!"})

        if password != c_password:
            return JsonResponse({'error_message': "Les mots de passe ne correspondent pas!"})
        
        nom_img = img.name
        if not nom_img.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'error_message': "L'image choisie pour votre mission doit être au format PNG, JPG ou JPEG."})

        if Add_admin.objects.filter(email=email).exists():
            return JsonResponse({'error_message': "Cet email existe déjà."})
        
        email_valide = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(email_valide, email):
            return JsonResponse({'error_message': "L'adresse e-mail que vous avez saisie n'est pas valide!"})

        admi = Add_admin(
            nom=nom, 
            prenom=prenom, 
            email=email, 
            img=img, 
            password= make_password(password)
            )
        admi.save()
        
        message_success = {
            "success" : True,
            "message" : f"Le compte de {nom} a été bien créé. Merci pour votre confiance!"
        }
        return JsonResponse(message_success)
    context = {'user': user}
    return render(request, 'Dashadmin/ajouter_admin.html', context)

def pub_mission(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = Add_admin.objects.get(pk=user_id) 
        except Add_admin.DoesNotExist:
            pass 

    if request.method == 'POST':
        theme = request.POST.get('theme')
        date = request.POST.get('date')
        img_mission = request.FILES.get('img_mission')
        lien = request.POST.get('lien')
        description = request.POST.get('description')
        
        if not all([theme, date, img_mission]):
            return JsonResponse({'error_message': "Seuls les champs lien et description ne sont pas obligatoires!"})
        
        nom_img = img_mission.name
        if not nom_img.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'error_message': "L'image choisie pour votre mission doit être au format PNG, JPG ou JPEG."})

        if lien:
            # Expression régulière pour valider les liens Facebook et YouTube
            facebook_regex = r'^(https?:\/\/)?(www\.)?facebook\.com\/.*$'
            youtube_regex = r'^(https?:\/\/)?(www\.)?youtube\.com\/.*$'
            
            if not (re.match(facebook_regex, lien, re.IGNORECASE) or re.match(youtube_regex, lien, re.IGNORECASE)):
                return JsonResponse({'error_message': "Le lien doit être une URL valide Facebook ou YouTube."}, status=400)
            
        mission = Add_mission(
            theme=theme, 
            date=date, 
            img_mission=img_mission, 
            lien=lien, 
            description=description
            )
        mission.save()
        
        message_success = {
            "success" : True,
            "message" : "Votre publication a été bien envoyé. Merci pour votre confiance!"
        }
        return JsonResponse(message_success)
    publication = Add_mission.objects.all()
    context = {'user': user, 'publication': publication}
    return render(request, 'Dashadmin/pub_mission.html', context)

def pub_annonce_FB(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = Add_admin.objects.get(pk=user_id) 
        except Add_admin.DoesNotExist:
            pass 

    if request.method == 'POST':
        theme_fb = request.POST.get('theme_fb')
        date_fb = request.POST.get('date_fb')
        img_fb = request.FILES.get('img_fb')
        lien_fb = request.POST.get('lien_fb')
        description_fb = request.POST.get('description_fb')
        
        if not all([theme_fb, date_fb, img_fb]):
            return JsonResponse({'error_message': "Seuls les champs lien et description ne sont pas obligatoires!"})
        
        nom_img = img_fb.name
        if not nom_img.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'error_message': "L'image choisie pour votre mission doit être au format PNG, JPG ou JPEG."})

        if lien_fb:
            # Expression régulière pour valider les liens Facebook et YouTube
            facebook_regex = r'^(https?:\/\/)?(www\.)?facebook\.com\/.*$'
            youtube_regex = r'^(https?:\/\/)?(www\.)?youtube\.com\/.*$'
            
            if not (re.match(facebook_regex, lien_fb, re.IGNORECASE) or re.match(youtube_regex, lien_fb, re.IGNORECASE)):
                return JsonResponse({'error_message': "Le lien doit être une URL valide Facebook ou YouTube."}, status=400)
            
        annonce_fb = Add_pubfb(
            theme_fb=theme_fb, 
            date_fb=date_fb, 
            img_fb=img_fb, 
            lien_fb=lien_fb, 
            description_fb=description_fb
            )
        annonce_fb.save()
        
        message_success = {
            "success" : True,
            "message" : "Votre annonce FB a été bien envoyé. Merci pour votre confiance!"
        }
        return JsonResponse(message_success)
    context = {'user': user}
    return render(request, 'Dashadmin/pub_annonce_FB.html', context)

def liste_avis(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = Add_admin.objects.get(pk=user_id) 
        except Add_admin.DoesNotExist:
            pass 

    avis =  Contact.objects.all()
    context = {
        'avis' : avis, 
        'user': user
        }
    return render(request, 'Dashadmin/liste_avis.html', context)

def supprimer_pub(request, publication_id):
    publication = get_object_or_404(Add_mission, id=publication_id)
    if request.method == 'POST':
        publication.delete()
        messages.success(request, "La publication a bien été supprimée.")
        return JsonResponse({'success': True})
    # Si ce n'est pas une requête POST, on retourne une erreur
    return JsonResponse({'success': False, 'error': 'Erreur lors de la suppression.'})

def modifier_mission(request):
    if request.method == 'POST':
        mission_id = request.POST.get('id')
        nv_theme = request.POST.get('nv_theme')
        nv_lien = request.POST.get('nv_lien')
        nv_description = request.POST.get('nv_description')
        nv_img_mission = request.FILES.get('nv_img_mission')

        if not all([nv_theme, nv_lien, nv_description]):
            return JsonResponse({'error_message': "Les champs ne doivent pas etre vides."}, status=400)

        try:
            mission = Add_mission.objects.get(id=mission_id)
            mission.theme = nv_theme
            mission.lien = nv_lien
            mission.description = nv_description

            if nv_img_mission:
                if not nv_img_mission.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return JsonResponse({'error_message': "Format d'image non supporté."})
                mission.img_mission = nv_img_mission
            
            mission.save()
            return JsonResponse({'success': True, 'message': f"Publication n°{mission_id} a été modifiée avec succès."})
        except Add_mission.DoesNotExist:
            return JsonResponse({'error_message': f"Publication n°{mission_id} non trouvée."}, status=404)
