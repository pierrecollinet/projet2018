# -*- coding: utf-8 -*-
from django.contrib import admin
from projetpaques2018.models import Utilisateur, Avion, Vol, Booking, RatingConducteur, Ville, Message, BookingEscale

admin.site.register(Utilisateur)
admin.site.register(Avion)
admin.site.register(Vol)
admin.site.register(Ville)
admin.site.register(Booking)
admin.site.register(BookingEscale)


admin.site.register(RatingConducteur)
admin.site.register(Message)
