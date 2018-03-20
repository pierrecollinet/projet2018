# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Utilisateur, Trajet, Booking, RatingConducteur

admin.site.register(Utilisateur)
admin.site.register(Trajet)
admin.site.register(Booking)
admin.site.register(RatingConducteur)