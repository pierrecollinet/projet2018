# -*- coding: utf-8 -*-

"""projetpaques2018 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-
from django.conf.urls import  include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

from projetpaques2018.views import bienvenue, signup, login, logout,    show_profile, evaluer_conducteur, modify_profile, voir_profil,chat_solvay, like, change_mdp,voir_ratings
# Employés urls
from projetpaques2018.views import nouvel_avion, employe_page, nouveau_vol, tableau_de_bord_employe

# Passagers views
from projetpaques2018.views import search, book, tableau_de_bord_passager, passager_page

urlpatterns = [
    url(r'^$', bienvenue),
    url(r'^bienvenue/$', bienvenue),

    # Employés url
    url(r'^nouvel-avion', nouvel_avion),
    url(r'^employe-page', employe_page),
    url(r'^nouveau-vol', nouveau_vol),
    url(r'^tableau-de-bord-employe', tableau_de_bord_employe),

    # Passagers url
    url(r'^passager-page', passager_page),
    url(r'^search', search),
    url(r'^book', book),
    url(r'^tableau-de-bord-passager', tableau_de_bord_passager),

    # urls communes aux 2 utilisateurs
    url(r'^signup', signup),
    url(r'^login', login),
    url(r'^logout', logout),

    url(r'^profil', show_profile),
    url(r'^modifier-profil/$', modify_profile),
    url(r'^voir-profil/$', voir_profil),
    url(r'^evaluer-conducteur/$', evaluer_conducteur),
    url(r'^chat-solvay/$', chat_solvay),
    url(r'^like/$', like),
    url(r'^change-mdp/$', change_mdp),
    url(r'^voir-ratings/$', voir_ratings),

    url(r'^admin/', include(admin.site.urls)),

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})

from django.conf import settings
import os
from django.views.static import serve as staticserve

# urlpatterns += ('',
#         (r'^static/(?P<path>.*)$', staticserve,
#             {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
#         )
#

