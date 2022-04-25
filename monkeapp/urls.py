from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='Home'),
    path('register', views.register_page, name='Rejestracja'),
    path('login', views.login_page, name='Login'),
    path('logout', views.logout_request, name='Logout'),
    path('get_gorilla', views.get_gorilla, name='Get Gorilla'),
    path('equipment', views.equipment, name="Equipment"),
    path('training', views.train_gorilla, name="Training"),
    path('actionUrl', views.buff_gorilla, name="Buff"),
    path('pve_combat', views.pve_combat, name="PvE"),
    path('pve_combat/<int:pk>', views.combat, name='fight'),
    path('pvp_gorillas', views.pvp_gorillas, name='pvp'),
    path('pop_upmonkey/<int:pk>', views.gorilla_windows, name="gorilla_window")
]