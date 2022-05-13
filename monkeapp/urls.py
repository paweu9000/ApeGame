from django.urls import path

from . import views, authorizationviews, menuoptions, combat, shoutbox
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.homepage, name='Home'),
    path('register', authorizationviews.register_page, name='Rejestracja'),
    path('login', authorizationviews.login_page, name='Login'),
    path('logout', authorizationviews.logout_request, name='Logout'),
    path('get_gorilla', menuoptions.get_gorilla, name='Get Gorilla'),
    path('equipment', menuoptions.equipment, name="Equipment"),
    path('training', menuoptions.train_gorilla, name="Training"),
    path('actionUrl', menuoptions.buff_gorilla, name="Buff"),
    path('actionUrl2', menuoptions.buff_gorilla_hp, name="Buff_hp"),
    path('auctions', menuoptions.auction_house, name="Auctions"),
    path('gorilla_options', menuoptions.gorilla_options, name="Gorilla Options"),
    path('gorilla_options/feed', menuoptions.feed_gorilla, name="Feed"),
    path('gorilla_options/stats', menuoptions.show_stats, name="stats"),
    path('gorilla_options/change_name', menuoptions.name_change, name="change_name"),
    path('user_profile/<int:pk>', menuoptions.user_profile, name="profile"),
    path('letters', menuoptions.letters, name='letters'),
    path('letters/send', menuoptions.send_letter, name='send'),
    path('letters/<int:pk>', menuoptions.letter_content, name='read_letter'),
    path('gorilla_options/edit_profile', menuoptions.edit_profile, name="edit"),
    path('gorilla_options/buy_bananas', menuoptions.buy_bananas, name='golden_bananas'),
    path('complete/', menuoptions.paymentComplete, name="complete"),
    path('auctions/<int:amount>/<int:pk>', menuoptions.buy_item, name='buy'),
    path('auctions/<str:itemname>/<int:pk>', menuoptions.cancel_auction, name='cancel'),
    path('pve_combat', combat.pve_combat, name="PvE"),
    path('pve_combat/<int:pk>', combat.combat, name='fight'),
    path('pvp_gorillas', combat.pvp_gorillas, name='pvp'),
    path('pop_upmonkey/<int:pk>', views.gorilla_windows, name="gorilla_window"),
    path('pop_upmonkey/<int:pk>/pvp', views.gorilla_windows_pvp, name="gorilla_window_pvp"),
    path('pvp_gorillas/<int:pk>', combat.pvp_combat, name='pvp_fight'),
    path('shoutbox', shoutbox.shoutbox_main, name='shoutbox'),
    path('shoutbox/message', shoutbox.new_message, name='message'),
    path('shoutbox/get_messages', shoutbox.get_messages, name='get_messages')
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)