# -*- coding: utf-8 -*-
from django.contrib import admin
from projetpaques2018.models import Utilisateur, Trajet, Booking, RatingConducteur, Ville, Message

admin.site.register(Utilisateur)
admin.site.register(Ville)
admin.site.register(Trajet)
admin.site.register(Booking)
admin.site.register(RatingConducteur)
admin.site.register(Message)
