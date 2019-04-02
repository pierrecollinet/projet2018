# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from projetpaques2018.models import Utilisateur, Avion, Vol, Booking, BookingEscale,    RatingConducteur, Ville, Message
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
        if request.POST :
            form_valid = True
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            statut = request.POST["statut"]
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
                                       password = password1,
                                       statut   = statut
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
        statut = user.statut
        # Si l'utilisateur est un employé
        if statut == "employe":
          return render(request, 'employe/welcome.html', {'current_user':user, 'villes':villes})
        # Si l'utilisateur est un passager
        else :
          return render(request, 'passager/welcome.html', {'current_user':user, 'villes':villes})
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

########################################
##########     EMPLOYE        ##########
########################################

def nouvel_avion(request):
    errors = []
    user = get_logged_user(request)

    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      # Si l'utilisateur n'est pas un pilote, on l'amène sur une page lui expliquand qu'il n'est pas pilote
      if user.statut == "passager" :
        return HttpResponseRedirect('/employe-page')
      # Sinon, on lui donne accès à la page demandée
      else :
        # Si le formulaire a été soumis :
        if request.POST :
          form_valid = True
          modele   = request.POST['modele']
          capacite = request.POST['capacite']
          if modele == "" or capacite == "":
            errors.append("Un des champs est vide")
            form_valid = False
          if not capacite.isdigit() or capacite <= 0 :
            errors.append("La capacité doit être un nombre entier positif")
            form_valid = False

          if form_valid :
            new_plane = Avion(
                            modele = modele,
                            capacite = capacite,
                            createur = user
                              )
            new_plane.save()
            return HttpResponseRedirect('/bienvenue')
          else :
            return render(request, 'employe/nouvel_avion.html', {'current_user':user,'modele':modele,'capacite':capacite, 'mes_erreurs':errors})
        return render(request, 'employe/nouvel_avion.html', {'current_user':user,'mes_erreurs':errors})
    # Si il n'est pas connecté, on l'invite à le faire
    else :
      return HttpResponseRedirect('/login')

def employe_page(request):
    errors = []
    user = get_logged_user(request)

    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      # Si l'utilisateur n'est pas un pilote, on l'amène sur une page lui expliquand qu'il n'est pas pilote
      if user.statut == "passager" :
        return render(request,'employe/employe_page.html', {'current_user':user})
      # Sinon, on lui donne accès à la page demandée
      else :
        return HttpResponseRedirect('/bienvenue')
    # Si il n'est pas connecté, on l'invite à le faire
    else :
      return HttpResponseRedirect('/login')

import datetime
def nouveau_vol(request):
    user = get_logged_user(request)
    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      if user.statut == "passager" :
        return HttpResponseRedirect('/employe-page')
      else :
        villes = Ville.objects.all()
        avions = Avion.objects.all()
        errors =[]
        today=datetime.datetime.now()
        #Si le formulaire est envoyé
        if request.POST :
            # Si le formulaire n'est pas valide
            form_valid = True
            date_depart       = request.POST['date_depart']
            date_depart       = datetime.datetime.strptime(date_depart, '%Y-%m-%d')
            heure_depart      = request.POST['heure_depart']
            heure_arrivee     = request.POST['heure_arrivee']
            ville_depart      = Ville.objects.get(id=request.POST['ville_depart'])
            ville_arrivee     = Ville.objects.get(id=request.POST['ville_arrivee'])
            avion             = Avion.objects.get(id=request.POST['avion_id'])
            prix              = request.POST['prix']
            if date_depart == "" or heure_depart == "" or heure_arrivee == "" or prix == "" or ville_depart =="" or ville_arrivee =="":
                error = "Tu as oublié un/des champ(s)"
                errors.append(error)
                form_valid = False
            if ville_depart == ville_arrivee :
                error = "Tu ne peux pas avoir la même ville de départ et d'arrivée"
                errors.append(error)
                form_valid = False
            if date_depart  <= today :
                error = "Tu ne peux pas réserver un vol le jour même, ni dans le passé"
                errors.append(error)
                form_valid = False
            if not prix.isdigit() or prix <= 0 :
              errors.append("Le prix doit être un nombre entier positif")
              form_valid = False

            # Tous les vols de cet avion, ce jour là dont le départ se situe entre l'heure d'arrivee et de départ
            vols_1 = Vol.objects.filter(avion=avion, date_depart = date_depart, heure_depart__gte = heure_depart, heure_depart__lte = heure_arrivee)
            # Tous les vols de cet avion, ce jour là dont l'arrivée se situe entre l'heure d'arrivee et de départ
            vols_2 = Vol.objects.filter(avion=avion, date_depart = date_depart, heure_arrivee__gte = heure_depart, heure_arrivee__lte = heure_arrivee)
            if len(vols_1) > 0 or len(vols_2) > 0 :
              errors.append("L'avion est déjà réquisitionné sur un autre vol à ce moment-là'")
              form_valid = False
            #
            # ATTENTION : encore checker LA CAPACITE (via bookings)
            #
            # Si le formulaire est valide
            if form_valid :
                # On sauve le trajet dans la DB
                new_vol = Vol(
                                    date_depart = date_depart,
                                    heure_depart = heure_depart,
                                    heure_arrivee = heure_arrivee,
                                    ville_depart = ville_depart,
                                    ville_arrivee = ville_arrivee,
                                    avion = avion,
                                    prix = prix,
                                    createur = user
                                    )
                new_vol.save()
                # On redirige vers la welcome page
                return HttpResponseRedirect('/bienvenue')
      return render(request,'employe/nouveau-vol.html', {'avions':avions,'villes':villes,'mes_erreurs':errors, "today":today, 'current_user':user})


    else :
      return HttpResponseRedirect('/login')

def tableau_de_bord_employe(request):
    user = get_logged_user(request)
    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      if user.statut == "passager" :
        return HttpResponseRedirect('/employe-page')
      else :
        vols = Vol.objects.all()
        return render(request,'employe/tableau-de-bord.html', {'vols':vols, 'current_user':user})
    else :
      return HttpResponseRedirect('/login')



########################################
##########     PASSAGER        ##########
########################################

def passager_page(request):
    errors = []
    user = get_logged_user(request)

    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      # Si l'utilisateur n'est pas un pilote, on l'amène sur une page lui expliquand qu'il n'est pas pilote
      if user.statut == "employe" :
        return render(request,'passager/passager_page.html', {'current_user':user})
      # Sinon, on lui donne accès à la page demandée
      else :
        return HttpResponseRedirect('/bienvenue')
    # Si il n'est pas connecté, on l'invite à le faire
    else :
      return HttpResponseRedirect('/login')

def search(request):
    user = get_logged_user(request)
    if user :
        if user.statut == "passager":
          vols_indirects = []
          # Initialement on affiche tous les résultats
          today = date.today()
          vols = Vol.objects.filter(date_depart__gte = today)
          # On passe toutes les villes au template pour le champ "select" ville départ et arrivée
          villes = Ville.objects.all()
          context = {}
          # si l'utilisateur clique sur chercher
          nbre_places = 1
          if request.GET :
              if 'ville_depart' in request.GET :
                  ville_de_depart_id = request.GET['ville_depart']
                  ville_de_depart = Ville.objects.get(id=ville_de_depart_id)
                  if ville_de_depart != "":
                      context.update({'ville_depart':ville_de_depart})
                      vols = vols.filter(ville_depart=ville_de_depart)
              if 'ville_arrivee' in request.GET :
                  ville_arrivee_id = request.GET['ville_arrivee']
                  ville_arrivee = Ville.objects.get(id=ville_arrivee_id)
                  if ville_arrivee != "":
                      context.update({'ville_arrivee':ville_arrivee})
                      vols = vols.filter(ville_arrivee=ville_arrivee)

              if 'heure_depart' in request.GET :
                  heure_depart = request.GET['heure_depart']
                  if heure_depart != "" :
                      context.update({'heure_depart':heure_depart})
                      vols = vols.filter(heure_depart=heure_depart)
              if 'date_depart' in request.GET :
                  date_depart  = request.GET['date_depart']
                  if date_depart != "":
                      context.update({'date_depart':date_depart})
                      vols = vols.filter(date_depart=date_depart)
              if 'capacite' in request.GET :
                  capacite =  request.GET['capacite']
                  if capacite != "":
                      context.update({'capacite':capacite})
                      vols = vols.filter(avion__capacite__gte = capacite)
                      nbre_places = capacite
              # Recherche des vols indirects
              if ville_arrivee and ville_de_depart :
                # On recherche tous les vols qui partent de la ville de départ ce jour-là
                vols_indirects_depart = Vol.objects.filter(ville_depart=ville_de_depart)
                # Ensuite pour chacun de ces vols, on regarde si il y en a un qui arrive à ville d'arrivée
                for v in vols_indirects_depart :
                  # 1. On regarde où il atterit
                  ville = v.ville_arrivee
                  # 2. On filtre les vols qui partent de "ville" et arrivent à la ville demandées
                  vols_indirect = Vol.objects.filter(ville_depart=ville, ville_arrivee=ville_arrivee)
                  if len(vols_indirect) > 0 :
                    vols_indirects.append({'vol1':v, 'vol2':vols_indirect.first()})
          context.update({'nbre_places':nbre_places, 'current_user':user, 'vols':vols, 'villes':villes, 'vols_indirects':vols_indirects})
          return render(request, 'search.html', context)
        else :
          return HttpResponseRedirect('/passager-page')
    else :
        return HttpResponseRedirect('/login')

def book(request):
    user = get_logged_user(request)
    errors = []
    today = date.today()
    vols = Vol.objects.filter(date_depart__gte = today)
    villes = Ville.objects.all()
    if user :
      if user.statut == "passager":
          form_valid = True
          # VOL DIRECT
          escale = request.POST['escale']
          if escale == "0" :
            vol_id = request.POST['vol_id']
            vol = Vol.objects.get(id = vol_id)
            nbre_places = request.POST['nbre_places']
            # 1°. Vérifier que le formulaire est valide
            # A. Vérifier qu'il y a de la place
            nombre_de_places_disponibles = vol.avion.capacite
            bookings_of_this_flight      = Booking.objects.filter(vol=vol)
            nombre_de_places_reservees   = 0
            for b in bookings_of_this_flight :
              nombre_de_places_reservees += b.nombre_de_places
            nombre_de_places_demandees   = nbre_places
            if int(nombre_de_places_disponibles) - nombre_de_places_reservees < int(nombre_de_places_demandees) :
                error = "Il ne reste que " + str(int(nombre_de_places_disponibles) - nombre_de_places_reservees) + " places (pas " + str(nombre_de_places_demandees) + ')'
                errors.append(error)
                form_valid = False
            # B. Vérifier que le trajet n'est pas déjà passé
            if vol.date_depart <= today :
                error = "Tu ne peux pas réserver dans le passé ou le jour même"
                errors.append(error)
                form_valid = False
            # 2°. Si le trajet est valide :
            if form_valid :
                new_booking = Booking(
                                    vol = vol,
                                    passager = user,
                                    nombre_de_places = nbre_places
                                    )
                new_booking.save()
                return HttpResponseRedirect('/tableau-de-bord-passager')
            # 3°. Si il n'est pas valide --> message d'erreur et redirect vers booking page
            else :
                return render(request, 'search.html', {'current_user':user, 'vols':vols, 'mes_erreurs':errors, 'villes':villes, 'nbre_places':nbre_places})
            # 3°. Si le formulaire est valide --> On crée une nouvelle reservation dans la DB et redirect vers ma profile page
          elif escale == "1":
                vol1 = Vol.objects.get(id=request.POST['vol1_id'])
                vol2 = Vol.objects.get(id=request.POST['vol2_id'])
                new_booking = BookingEscale(
                                    vol1 = vol1,
                                    vol2 = vol2,
                                    passager = user,
                                    nombre_de_places = request.POST['nbre_places']
                                    )
                new_booking.save()
                return HttpResponseRedirect('/tableau-de-bord-passager')
      else :
          return HttpResponseRedirect('/passager-page')
    else :
        return HttpResponseRedirect('/login')

def tableau_de_bord_passager(request):
    user = get_logged_user(request)
    # Si l'utilisateur est déjà connecté, on lui donne accès à la page demandée
    if user :
      if user.statut == "employe" :
        return HttpResponseRedirect('/passager-page')
      else :
        vols = Vol.objects.all()
        reservations = Booking.objects.filter(passager = user)
        reservations_indirectes = BookingEscale.objects.filter(passager = user)
        return render(request,'passager/tableau-de-bord.html', {'reservations_indirectes':reservations_indirectes,'reservations':reservations,'vols':vols, 'current_user':user})
    else :
      return HttpResponseRedirect('/login')







def show_profile(request):
    user = get_logged_user(request)
    if user :
        if 'user_id' in request.GET :
            user_id = request.GET['user_id']
            user_to_show = Utilisateur.objects.get(id=user_id)
        return render(request,'show-profile.html', {'current_user':user, 'user_to_show':user_to_show})
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
    #    ratings = RatingConducteur.objects.filter(trajet__in = Trajet.objects.filter(conducteur=user_to_show))
    #    moyenne_proprete = 0
    #    moyenne_ponctualite = 0
    #    for r in ratings :
    #        moyenne_proprete += int(r.proprete)
    #        moyenne_ponctualite += int(r.ponctualite)
    #    if len(ratings) > 0:
    #        moyenne_proprete    = moyenne_proprete/len(ratings)
    #        moyenne_ponctualite = moyenne_ponctualite/len(ratings)
        return render(request, 'voir-profil.html', {"user_to_show": user_to_show, 'current_user':current_user})
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

def code_ressource(request):
    return render (request, "code_ressource.html", {})






