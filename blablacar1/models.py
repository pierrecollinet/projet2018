# -*- coding: utf-8 -*-

from django.db import models

class Utilisateur(models.Model):
    username = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank = True, null = True)
    nom = models.CharField(max_length=100, blank = True, null = True)
    password = models.CharField(max_length=100)
    like = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom
    
class Trajet(models.Model):
    date_depart = models.DateField(blank=True,null=True)
    heure_depart = models.TimeField(blank=True,null=True)
    ville_depart = models.ForeignKey(Ville,blank=True,null=True, related_name = "ville_depart")
    ville_arrivee = models.ForeignKey(Ville,blank=True,null=True, related_name = "ville_arrivee")
    capacite = models.PositiveSmallIntegerField()
    prix_par_personne = models.CharField(max_length=100)
    conducteur = models.ForeignKey(Utilisateur)
    marque_voiture = models.CharField(max_length=100, blank=True,null=True)
    
    def __str__(self):
        return self.ville_depart.nom + ' a ' + self.ville_arrivee.nom    
    
class Booking(models.Model):
    trajet = models.ForeignKey(Trajet)
    passager = models.ForeignKey(Utilisateur)
    is_paid = models.BooleanField(default = False)
    
    def __str__(self):
        return self.passager.username + ' - de ' + self.trajet.ville_depart  + ' a ' + self.trajet.ville_arrivee     
 
class RatingConducteur(models.Model):
    trajet = models.ForeignKey(Trajet)
    auteur = models.ForeignKey(Utilisateur)
    proprete = models.CharField(max_length=100)
    ponctualite = models.CharField(max_length=100)
    commentaire = models.TextField()
    
    def __str__(self):
        return self.auteur.username + ' par rapport a ' + self.trajet.conducteur.username 

class Message(models.Model):
    message = models.TextField()
    auteur = models.ForeignKey(Utilisateur)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.auteur.username 