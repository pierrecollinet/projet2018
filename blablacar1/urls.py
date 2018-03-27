# -*- coding: utf-8 -*-

"""blablacar1 URL Configuration

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

from blablacar1.views import bienvenue, signup, login, nouveau_trajet, logout, show_profile, search, book, evaluer_conducteur, modify_profile, voir_profil

urlpatterns = [
    url(r'^$', bienvenue),
    url(r'^bienvenue/$', bienvenue),
    url(r'^signup/$', signup),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^profil/$', show_profile),
    url(r'^nouveau-trajet/$', nouveau_trajet),
    url(r'^search/$', search),
    url(r'^modifier-profil/$', modify_profile),
    url(r'^book/$', book),
    url(r'^voir-profil/$', voir_profil),
    url(r'^evaluer-conducteur/$', evaluer_conducteur),
    
    url(r'^admin/', include(admin.site.urls)),
    
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})