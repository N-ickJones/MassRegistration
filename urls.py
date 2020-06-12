# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from django.views.i18n import JavaScriptCatalog

import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Home Page
    path('', views.home, name='home'),

    # Include the Django Authentication default login/logout
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    # Include the App Urls
    path('', include('registration.urls', namespace='registration')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    # Adds Admin Widgets for Forms
    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),

] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
