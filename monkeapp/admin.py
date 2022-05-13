from django.contrib import admin

from .models import Room, Message, Gorilla, TrainingTimer, Profile, Letter, Auction, Opponent, Equipment

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Gorilla)
admin.site.register(TrainingTimer)
admin.site.register(Profile)
admin.site.register(Letter)
admin.site.register(Auction)
admin.site.register(Opponent)
admin.site.register(Equipment)
