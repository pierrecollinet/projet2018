# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from blablacar1.models import Utilisateur, Trajet, Booking, RatingConducteur, Ville, Message
from datetime import date

def get_logged_user(request):
    if "user_id" in request.session and len(Utilisateur.objects.filter(id=request.session["user_id"])) == 1  : 
        user = Utilisateur.objects.get(id=request.session["user_id"])
        return user
    else : 
        return None
        
def logout(request):
    del request.session['user_id']
    return HttpResponseRedirect('/login')   
 
def signup(request):
    errors = []
    user = get_logged_user(request)
    
    # Si l'utilisateur est déjà connecté, on le redirige vers la welcome page
    if user :
        return HttpResponseRedirect('/bienvenue')
    # Sinon, il arrive sur la page de signup (comme prévu)
    else : 
        # Si l'utilisateur a appuyé sur submit
        if request.GET : 
            form_valid = True
            username = request.GET["username"]
            password1 = request.GET["password1"]
            password2 = request.GET["password2"]
            # 1. Vérifier que les champs introduis sont corrects
            if username == "" :
                form_valid = False
                error = "Tu as oublié de compléter ton nom d'utilisateur"
                errors.append(error)
            if password1 == "" : 
                form_valid = False
                error = "Tu as oublié de compléter ton password"
                errors.append(error)
            if password2 == "" : 
                form_valid = False
                error = "Tu as oublié de compléter ton password2"
                errors.append(error)
            if password1 != password2 : 
                form_valid = False
                error = "Introduis 2 passwords identiques stp"
                errors.append(error)             
            if len(Utilisateur.objects.filter(username=username)) > 0 : 
                form_valid = False
                error = "il y a déjà un utilisateur avec ce username. Essaie en un autre"
                errors.append(error)                   
            # 2. Si champs corrects --> sauver un nouvel utilisateur et rediriger vers login
            if form_valid : 
                # A. Sauver un nouvel utilisateur dans DB
                new_user = Utilisateur(username = username,
                                       password = password1
                                       )
                new_user.save()
                
                # B. Rediriger vers la page de login
                return HttpResponseRedirect("/login")
            else : 
                return render(request, 'signup.html', {'mes_erreurs':errors, 'username':username, 'password1':password1})  
        # 3. Sinon, recharger la même page
        return render(request,'signup.html', {'mes_erreurs':errors})        

def bienvenue(request):
    if "user_id" in request.session and len(Utilisateur.objects.filter(id=request.session["user_id"])) == 1 :
        # On va "chercher" toutes les villes pour les mettre dans le champ "ville" du formulaire (select button)
        villes = Ville.objects.all() 
        user = Utilisateur.objects.get(id=request.session["user_id"])
        return render(request, 'welcome.html', {'current_user':user, 'villes':villes})
    else : 
        return HttpResponseRedirect('/login')
   
def login(request):
    errors = []
    user = get_logged_user(request)
    
    # Si l'utilisateur est déjà connecté, on le redirige vers la welcome page
    if user :
        return HttpResponseRedirect('/bienvenue')
    # Sinon, il arrive sur la page de signup (comme prévu)
    else : 
        # Si le formulaire est envoyé == si l'utilisateur clique sur se connecter
        if request.POST : 
            username = request.POST['username']
            password = request.POST['password']
            # Si le formulaire n'est pas valide
            users = Utilisateur.objects.filter(username=username, password=password)
            if len(users) != 1 : 
                error = "mdp ou username erroné"
                errors.append(error)
                # Alors on renvoie vers la page login avec un message d'erreur
            # Si le formulaire est valide 
            else : 
                # on "retient" cet utilisateur
                current_user = Utilisateur.objects.get(username=username, password=password)
                request.session['user_id'] = current_user.id
                return HttpResponseRedirect('/bienvenue')
            # Alors on renvoie vers la page welcome
            
        # Si le formulaire n'est pas envoyé
        return render(request, 'login.html', {'mes_erreurs':errors})

import datetime
def nouveau_trajet(request):
    villes = Ville.objects.all()
    user_id = request.session['user_id']
    current_user = Utilisateur.objects.get(id=user_id)
    errors =[]
    today=datetime.datetime.now()
    #Si le formulaire est envoyé
    if request.POST : 
        # Si le formulaire n'est pas valide
        form_valid = True
        date_depart       = request.POST['date_depart']
        heure_depart      = request.POST['heure_depart']
        capacite          = request.POST['capacite']
        prix_par_personne = request.POST['prix_par_personne'] 
        if date_depart == "" or heure_depart == "" or capacite == "" or prix_par_personne == "" :      
            error = "Tu as oublié un/des champ(s)"
            errors.append(error)
            form_valid = False
        if "ville_arrivee" in request.POST and "ville_depart"  in request.POST : 
            ville_depart_id   = request.POST['ville_depart']
            ville_depart      = Ville.objects.get(id=ville_depart_id)
            ville_arrivee_id  = request.POST['ville_arrivee']
            ville_arrivee     = Ville.objects.get(id=ville_arrivee_id)
        else : 
            error = "Tu dois sélectionner une ville de départ et une ville d'arrivée"
            errors.append(error)
            form_valid = False            
        # Si le formulaire est valide
        if form_valid :
            # On sauve le trajet dans la DB
            new_trajet = Trajet(
                                date_depart = date_depart,
                                heure_depart = heure_depart,
                                ville_depart = ville_depart,
                                ville_arrivee = ville_arrivee,
                                capacite = capacite,
                                prix_par_personne = prix_par_personne,
                                conducteur = current_user                       
                                )
            new_trajet.save()
            # On redirige vers la welcome page
            return HttpResponseRedirect('/bienvenue')
    return render(request,'nouveau-trajet.html', {'villes':villes,'mes_erreurs':errors, "today":today, 'current_user':current_user})

def show_profile(request):
    user = get_logged_user(request)
    if user : 
        if 'user_id' in request.GET : 
            user_id = request.GET['user_id']
            user_to_show = Utilisateur.objects.get(id=user_id)
        return render(request,'show-profile.html', {'current_user':user, 'user_to_show':user_to_show})
    else : 
        return HttpResponseRedirect('/login')

def search(request):
    user = get_logged_user(request)
    if user :
        # Initialement on affiche tous les résultats
        today = date.today()
        trajets = Trajet.objects.filter(date_depart__gte = today)
        # On passe toutes les villes au template pour le champ "select" ville départ et arrivée
        villes = Ville.objects.all()
        # si l'utilisateur clique sur chercher
        if request.GET :
            if 'ville_depart' in request.GET : 
                ville_de_depart_id = request.GET['ville_depart']
                ville_de_depart = Ville.objects.get(id=ville_de_depart_id)
                if ville_de_depart != "":
                    trajets = trajets.filter(ville_depart=ville_de_depart)
            if 'ville_arrivee' in request.GET : 
                ville_arrivee_id = request.GET['ville_arrivee']
                ville_arrivee = Ville.objects.get(id=ville_arrivee_id)
                if ville_arrivee != "":
                    trajets = trajets.filter(ville_arrivee=ville_arrivee)
            
            if 'heure_depart' in request.GET : 
                heure_depart = request.GET['heure_depart']
                if heure_depart != "" : 
                    trajets = trajets.filter(heure_depart=heure_depart)
            if 'date_depart' in request.GET : 
                date_depart  = request.GET['date_depart']
                if date_depart != "":
                    trajets = trajets.filter(date_depart=date_depart)
              
            if 'capacite' in request.GET : 
                capacite =  request.GET['capacite']
                if capacite != "":
                    trajets = trajets.filter(capacite__gte = capacite)
        return render(request, 'search.html', {'current_user':user, 'trajets':trajets, 'villes':villes})
    else : 
        return HttpResponseRedirect('/login')

def book(request):
    user = get_logged_user(request)
    errors = []
    today = date.today()
    trajets = Trajet.objects.filter(date_depart__gte = today)
    if user :
        form_valid = True
        trajet_id = request.GET['trajet_id']
        trajet = Trajet.objects.get(id = trajet_id)
        # 1°. Vérifier que le formulaire est valide
        # A. Vérifier qu'il y a de la place
        nombre_de_places_initiales = trajet.capacite
        reservation_de_ce_trajet = Booking.objects.filter(trajet=trajet)
        nombre_de_places_deja_reservees = len(reservation_de_ce_trajet)
        # B. Vérifier qu'il n'est pas conducteur
        if nombre_de_places_deja_reservees >= nombre_de_places_initiales : 
            error = "Tu ne peux pas réserver, il n'y a plus de places"
            errors.append(error)
            form_valid = False
        if trajet.conducteur == user : 
            error = "Tu ne peux pas réserver puisque tu es déjà conducteur"
            errors.append(error)
            form_valid = False
        # C. Vérifier que le trajet n'est pas déjà passé
        if trajet.date_depart < today : 
            error = "Tu ne peux pas réserver dans le passé"
            errors.append(error)
            form_valid = False
        # 2°. Si le trajet est valide : 
        if form_valid : 
            new_booking = Booking(
                                trajet = trajet,
                                passager = user
                                )
            new_booking.save()
            return HttpResponseRedirect('/voir-profil?user_id='+str(user.id))
        # 3°. Si il n'est pas valide --> message d'erreur et redirect vers booking page
        else : 
            return render(request, 'search.html', {'current_user':user, 'trajets':trajets, 'mes_erreurs':errors})
        # 3°. Si le formulaire est valide --> On crée une nouvelle reservation dans la DB et redirect vers ma profile page
        
    else : 
        return HttpResponseRedirect('/login')
    
    
def evaluer_conducteur(request):
    user = get_logged_user(request)
    errors = []
    if user :
        trajet_id = request.GET['trajet_id']
        trajet = Trajet.objects.get(id=trajet_id)
        # Si l'utilisateur clique sur confirmer
        if request.POST : 
            form_valid = True
            ponctualite = request.POST['ponctualite']
            proprete = request.POST['proprete']
            commentaire = request.POST['commentaire']
            if len(RatingConducteur.objects.filter(auteur=user, trajet=trajet)) > 0 :
                form_valid = False
                error = "Tu as déjà évalué cette course"
                errors.append(error)
            
            if form_valid : 
                new_rating = RatingConducteur(
                                            trajet = trajet,
                                            auteur = user,
                                            proprete = proprete,
                                            ponctualite = ponctualite,
                                            commentaire = commentaire
                                            )
                new_rating.save()
                return HttpResponseRedirect('/bienvenue')
                
        return render(request, 'evaluer-conducteur.html', {'current_user':user, 'trajet':trajet, 'mes_erreurs':errors})       
    else : 
        return HttpResponseRedirect('/login')    
    
def modify_profile(request):
    user_id = request.session['user_id']
    user = Utilisateur.objects.get(id=user_id)
    if user : 
        # si l'utilisateur clique sur valider
        if request.POST : 
            # Valider les champs de formulaires
            # ...
            prenom = request.POST["prenom"]
            nom = request.POST["nom"]
            user.prenom = prenom
            user.nom = nom
            user.save()
            return HttpResponseRedirect('/bienvenue')
        return render(request, 'modifier-profil.html', {'current_user':user})
    else : 
        return HttpResponseRedirect('/login')

def voir_profil(request):
    if 'user_id' in request.session : 
        current_user = Utilisateur.objects.get(id=request.session['user_id'])
        user_to_show_id = request.GET['user_id']
        user_to_show = Utilisateur.objects.get(id = user_to_show_id)
        ratings = RatingConducteur.objects.filter(trajet__in = Trajet.objects.filter(conducteur=user_to_show))
        moyenne_proprete = 0
        moyenne_ponctualite = 0 
        for r in ratings : 
            moyenne_proprete += int(r.proprete)
            moyenne_ponctualite += int(r.ponctualite)
        return render(request, 'voir-profil.html', {'moyenne_proprete':moyenne_proprete,'moyenne_ponctualite':moyenne_ponctualite,"user_to_show": user_to_show, 'current_user':current_user})
    else : 
        return HttpResponseRedirect('/login')
    
def chat_solvay(request):
    if 'user_id' in request.session : 
        current_user = Utilisateur.objects.get(id=request.session['user_id'])
        form_valid = True
        errors = []
        messages = Message.objects.all().order_by('date')
        if request.POST :
            message =  request.POST['message']
            if message =="":
                form_valid = False
                error = "Tu ne peux pas envoyer un message vide..."
                errors.append(error)
                
            if form_valid :
                new_message = Message(message=message, auteur=current_user)
                new_message.save()
        if len(Message.objects.filter(auteur=current_user)) > 1 and current_user.like == False :
            show_modal = True
        else : 
            show_modal = False
        return render(request, 'chat-solvay.html', {'show_modal':show_modal,'messages':messages,'current_user':current_user, 'mes_erreurs':errors})
    else : 
        return HttpResponseRedirect('/login')

def like(request):
    if 'user_id' in request.session : 
        current_user = Utilisateur.objects.get(id=request.session['user_id'])
        current_user.like = True
        current_user.save()
        return HttpResponseRedirect('https://www.facebook.com/blocusassistance/')
    else : 
        return HttpResponseRedirect('/login')
    
def change_mdp(request):
    if 'user_id' in request.session : 
        current_user = Utilisateur.objects.get(id=request.session['user_id'])
        errors = []
        if request.POST : 
            form_valid = True
            old_mdp = request.POST["old_mdp"]
            new_mdp1 = request.POST["new_mdp1"]
            new_mdp2 = request.POST["new_mdp2"]
            if old_mdp != current_user.password : 
                error = "Ton ancien mot de passe n'est pas correct"
                errors.append(error)
                form_valid=False
            if new_mdp1 != new_mdp2 : 
                error = "Introduis 2 fois le même mot de passe"
                errors.append(error)
                form_valid=False
            if form_valid : 
                current_user.password = new_mdp1
                current_user.save()
                return HttpResponseRedirect('/voir-profil?user_id='+str(current_user.id))
        return render(request, 'change-mdp.html', {'current_user':current_user,'mes_erreurs':errors})
    else : 
        return HttpResponseRedirect('/login')

def voir_ratings(request):
    if 'user_id' in request.session : 
        current_user = Utilisateur.objects.get(id=request.session['user_id'])
        errors = []
        if 'user_id' in request.GET : 
            user = Utilisateur.objects.get(id=request.GET['user_id'])
            trajets = Trajet.objects.filter(conducteur = user)
            ratings = RatingConducteur.objects.filter(trajet__in = trajets)
        return render(request, 'voir-ratings.html', {'current_user':current_user,'mes_erreurs':errors, 'ratings':ratings})
    else : 
        return HttpResponseRedirect('/login')