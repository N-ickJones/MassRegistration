from . import views
from django.urls import path


app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),

    path('profile/', views.view_profile, name='view_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),

    path('parish/view/', views.view_parish, name='view_parish'),
    path('parish/add/', views.add_parish, name='add_parish'),
    path('parish/change/<int:parish_id>', views.change_parish, name='change_parish'),
    path('parish/delete/<int:parish_id>', views.delete_parish, name='delete_parish'),
    path('parish/select/', views.select_parish, name='select_parish'),
    path('parish/subscribe/', views.subscribe_parish, name='subscribe_parish'),

    path('mass/view/', views.view_mass, name='view_mass'),
    path('mass/add/', views.add_mass, name='add_mass'),
    path('mass/change/<int:mass_id>', views.change_mass, name='change_mass'),
    path('mass/delete/<int:mass_id>', views.delete_mass, name='delete_mass'),

    path('attendee/view/', views.view_attendee, name='view_attendee'),
    path('attendee/add/', views.add_attendee, name='add_attendee'),
    path('attendee/change/<int:attendee_id>', views.change_attendee, name='change_attendee'),
    path('attendee/delete/<int:attendee_id>', views.delete_attendee, name='delete_attendee'),

    path('phone/view/', views.view_phone, name='view_phone'),

]
