# -*- coding: utf-8 -*-
from django.contrib import admin
from blablacar1.models import Utilisateur, Trajet, Booking, RatingConducteur, Ville

admin.site.register(Utilisateur)
admin.site.register(Ville)
admin.site.register(Trajet)
admin.site.register(Booking)
admin.site.register(RatingConducteur)