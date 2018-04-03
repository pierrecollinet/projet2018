# -*- coding: utf-8 -*-

from django.db import models

class Utilisateur(models.Model):
    username = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank = True, null = True)
    nom = models.CharField(max_length=100, blank = True, null = True)
    password = models.CharField(max_length=100)
    like = models.BooleanField(default=False)
    statut = models.CharField(max_length=100, blank = True, null = True)

    def __str__(self):
        return self.username

    def get_statut(self):
        return self.statut

class Avion(models.Model) :
  createur = models.ForeignKey(Utilisateur)
  modele   = models.CharField(max_length=100)
  capacite = models.PositiveSmallIntegerField()

  def __str__(self):
    return self.modele + " - Ajouté par " + self.createur.username

class Ville(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Vol(models.Model):
    date_depart = models.DateField(blank=True,null=True)
    heure_depart = models.TimeField(blank=True,null=True)
    heure_arrivee = models.TimeField(blank=True,null=True)
    ville_depart = models.ForeignKey(Ville,blank=True,null=True, related_name = "ville_depart")
    ville_arrivee = models.ForeignKey(Ville,blank=True,null=True, related_name = "ville_arrivee")
    avion = models.ForeignKey(Avion)
    prix = models.CharField(max_length=100)
    createur = models.ForeignKey(Utilisateur, blank=True,null=True)

    def __str__(self):
        return self.ville_depart.nom + ' à ' + self.ville_arrivee.nom

    def calculate_revenu_total(self):
      total = 0
      for b in self.booking_set.all():
        total += b.calculate_price()
      return total

    def get_places_reservees(self):
      count = 0
      for b in self.booking_set.all():
        count += b.nombre_de_places
      return count

    def get_places_dispos(self):
      return self.avion.capacite - self.get_places_reservees()

class Booking(models.Model):
    vol = models.ForeignKey(Vol, blank=True,null=True)
    passager = models.ForeignKey(Utilisateur)
    is_paid = models.BooleanField(default = False)
    nombre_de_places = models.PositiveSmallIntegerField(blank=True,null=True)

    def __str__(self):
        return self.passager.username + ' - de ' + self.vol.ville_depart.nom  + ' à ' + self.vol.ville_arrivee.nom

    def calculate_price(self):
      return int(self.nombre_de_places) * float(self.vol.prix)

class BookingEscale(models.Model):
    vol1 = models.ForeignKey(Vol, related_name="vol1",blank=True,null=True)
    vol2 = models.ForeignKey(Vol, related_name="vol2",blank=True,null=True)
    passager = models.ForeignKey(Utilisateur)
    is_paid = models.BooleanField(default = False)
    nombre_de_places = models.PositiveSmallIntegerField(blank=True,null=True)

    def __str__(self):
        return self.passager.username + ' - de ' + self.vol1.ville_depart.nom  + ' à ' + self.vol2.ville_arrivee.nom

    def calculate_price(self):
      return int(self.nombre_de_places) * (float(self.vol1.prix) + float(self.vol2.prix))




class RatingConducteur(models.Model):
    vol = models.ForeignKey(Vol, blank=True,null=True)
    auteur = models.ForeignKey(Utilisateur)
    proprete = models.CharField(max_length=100)
    ponctualite = models.CharField(max_length=100)
    commentaire = models.TextField()

    def __str__(self):
        return self.auteur.username + ' par rapport a ' + self.vol.conducteur.username

class Message(models.Model):
    message = models.TextField()
    auteur = models.ForeignKey(Utilisateur)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.auteur.username
