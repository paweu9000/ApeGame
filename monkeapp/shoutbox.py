from django.shortcuts import render, redirect
from .models import Room, Message, User
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

def shoutbox_main(request):
    room = Room.objects.all().get(name='Shoutbox')
    username = request.user
    context = {
        'room': room,
        'username': username
    }
    return render(request, 'shoutbox/shoutboxmain.html', context=context)

def new_message(request):
    message = request.POST['message']
    username = request.POST['username']
    message_owner = User.objects.all().get(username=username)

    new_m = Message.objects.create(value=message, date=timezone.now(), message_owner=message_owner, user=username)
    new_m.save()
    return HttpResponse('Wiadomość wysłana!')

def get_messages(request):
    room_object = Room.objects.get(name='Shoutbox')

    messages = Message.objects.all().filter(room=room_object.name)[:20]
    return JsonResponse({"messages": list(messages.values())})