from . import views
from django.urls import path

app_name = 'registration'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/parishioner/', views.signup_parishioner, name='signup_parishioner'),
    path('signup/parish/', views.signup_parish, name='signup_parish'),

]
