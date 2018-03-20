# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.template import RequestContext

from blablacar1.models import Utilisateur, Trajet, Booking, RatingConducteur

def get_logged_user(request):
    if "user_id" in request.session : 
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
        
            # 2. Si champs corrects --> sauver un nouvel utilisateur et rediriger vers login
            if form_valid : 
                # A. Sauver un nouvel utilisateur dans DB
                new_user = Utilisateur(username = username,
                                       password = password1
                                       )
                new_user.save()
                
                # B. Rediriger vers la page de login
                return HttpResponseRedirect("/login")
        # 3. Sinon, recharger la même page
        return render_to_response('signup.html', {'mes_erreurs':errors})        

def bienvenue(request):
    if "user_id" in request.session : 
        user = Utilisateur.objects.get(id=request.session["user_id"])
        return render_to_response('welcome.html', {'current_user':user})
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
            print(users)
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
        return render_to_response('login.html', {'mes_erreurs':errors}, context_instance=RequestContext(request))

import datetime
def nouveau_trajet(request):
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
        ville_depart      = request.POST['ville_depart']
        ville_arrivee     = request.POST['ville_arrivee']
        capacite          = request.POST['capacite']
        prix_par_personne = request.POST['prix_par_personne'] 
        if date_depart == "" or heure_depart == "" or ville_depart == "" or ville_arrivee == "" or capacite == "" or prix_par_personne == "" :      
            error = "Tu as oublié un chamop"
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
    return render_to_response('nouveau-trajet.html', {'mes_erreurs':errors, "today":today}, context_instance=RequestContext(request))

def show_profile(request):
    user = get_logged_user(request)
    if user : 
        if 'user_id' in request.GET : 
            user_id = request.GET['user_id']
            user_to_show = Utilisateur.objects.get(id=user_id)
        return render_to_response('show-profile.html', {'current_user':user, 'user_to_show':user_to_show}, context_instance=RequestContext(request))
    else : 
        return HttpResponseRedirect('/login')

def search(request):
    user = get_logged_user(request)
    if user :
        # Initialement on affiche tous les résultats
        trajets = Trajet.objects.all()
        # Si l'utilisateur clique sur "chercher"
        if request.GET : 
            date_depart       = request.GET['date_depart']
            ville_depart      = request.GET['ville_depart']
            ville_arrivee     = request.GET['ville_arrivee']
            if "heure_depart" in request.GET : 
                heure_depart = request.GET['heure_depart']
            else : 
                heure_depart = ""
            if "capacite" in request.GET : 
                capacite = request.GET['capacite']
            else:
                capacite = ""
            
            # Si le champs n'est pas vide, c'est que l'utilisateur l'a complété et souhaite filtrer ce champ
            if date_depart != "":
                trajets = trajets.filter(date_depart = date_depart)
            if heure_depart != "":
                trajets = trajets.filter(heure_depart = heure_depart)
            if ville_depart != "":
                trajets = trajets.filter(ville_depart = ville_depart)
            if ville_arrivee != "":
                trajets = trajets.filter(ville_arrivee = ville_arrivee)
            if capacite != "":
                # Il faut une voiture pouvant accueillir AU MOINS le nombre de places demandées
                trajets = trajets.filter(capacite__gte = capacite)
        return render_to_response('search.html', {'current_user':user, 'trajets':trajets}, context_instance=RequestContext(request))
    else : 
        return HttpResponseRedirect('/login')

def book(request):
    user = get_logged_user(request)
    errors = []
    if user :
        # Si l'utilisateur clique sur "réserver"
        if request.GET :
            form_valid = True
            trajet_id = request.GET['trajet_id']
            trajet = Trajet.objects.get(id=trajet_id)
            # On récupère les réservations déjà existantes de ce trajet
            bookings = Booking.objects.filter(trajet=trajet)
            if len(bookings) >= trajet.capacite : 
                form_valid = False
                error = "Désolé mais ce trajet est déjà complet"
                errors.append(error)
                trajets = Trajet.objects.all()
            # On vérifie que l'utilisateur n'a pas déjà réservé ce trajet
            if len(Booking.objects.filter(passager=user)) > 0 : 
                form_valid = False
                error = "Tu as déjà effectué une réservation pour ce trajet"
                errors.append(error)
                trajets = Trajet.objects.all()   
            # On vérifie que l'utilisateur n'essaie pas de réserver SON PROPRE TRAJET
            if trajet.conducteur == user : 
                form_valid = False
                error = "Tu ne peux pas réserver ce trajet puisque c'est toi le conducteur"
                errors.append(error)
                trajets = Trajet.objects.all()            
            if form_valid : 
                new_booking = Booking(
                                    trajet = trajet,
                                    passager = user
                                    )
                new_booking.save()
            else : 
                return render_to_response('search.html', {'current_user':user, 'trajets':trajets, 'mes_erreurs':errors}, context_instance=RequestContext(request))
                
        return HttpResponseRedirect('/profil?user_id='+str(user.id))
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
                
        return render_to_response('evaluer-conducteur.html', {'current_user':user, 'trajet':trajet, 'mes_erreurs':errors}, context_instance=RequestContext(request))       
    else : 
        return HttpResponseRedirect('/login')    
    
    
    
