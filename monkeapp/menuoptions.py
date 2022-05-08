from django.dispatch import receiver
from django.shortcuts import render, redirect
from .forms import GorillaForm, LetterForm, ProfileForm
from django.contrib import messages
from .models import Gorilla, Equipment, Letter, Profile, TrainingTimer, Auction, User
from datetime import datetime, timedelta
from django.utils import timezone
from . import views
from django.http import JsonResponse
import json

def get_gorilla(request):
	if not request.user.is_authenticated:
		return redirect(views.homepage)
	if request.method == "POST":
		form = GorillaForm(request.POST)
		if form.is_valid():
			new_Gorilla = Gorilla(name=form.cleaned_data.get('name'))
			new_Gorilla.owner = request.user
			new_Gorilla.save()
			messages.success(request, f"You have just adopted gorilla!")
			return redirect(views.homepage)
		else: 
			messages.error(request, "Something went wrong")
	form = GorillaForm()
	return render(request, 'menupages/get_gorilla.html', context={"gorilla_form":form})

def equipment(request):
	if not request.user.is_authenticated:
		return redirect(views.homepage)
	items = Equipment.objects.all().get(equipment_owner=request.user.id)
	context = {
		'items': items
	}
	return render(request, 'menupages/equipment.html', context=context)

def train_gorilla(request):
	current_user = request.user
	all_gorillas = Gorilla.objects.all().get(owner=current_user)
	training_timer = None
	items = Equipment.objects.all().get(equipment_owner=request.user)
	try:
		if TrainingTimer.objects.all().get(trained_gorilla=all_gorillas).finished_training - timedelta(minutes=120) < timezone.now():
			TrainingTimer.objects.filter(trained_gorilla=all_gorillas).delete()
	except:
		pass
	try:
		training_timer = TrainingTimer.objects.all().get(trained_gorilla=all_gorillas)
		context = {
		'all_gorillas': all_gorillas,
		'items': items,
		'training_timer': training_timer
		}
		return render(request, 'menupages/training.html', context=context)
	except:
		context = {
			'all_gorillas': all_gorillas,
			'items': items,
			'training_timer': training_timer
		}
		return render(request, 'menupages/training.html', context=context)

def buff_gorilla(request):
	current_user = request.user
	gorilla_to_buff = Gorilla.objects.all().get(owner=current_user)
	equipment_to_delete = Equipment.objects.all().get(equipment_owner=current_user)
	try:
		training_timer = TrainingTimer.objects.all().get(trained_gorilla=gorilla_to_buff)
		if training_timer:
			messages.error(request, f"Your Gorilla is already training!")
			return redirect(train_gorilla)
	except:
		if equipment_to_delete.item1 >= 2 and equipment_to_delete.item3 >=5:
			new_timer = TrainingTimer(trained_gorilla=gorilla_to_buff)
			new_timer.save()
			equipment_to_delete.item1 -= 2
			equipment_to_delete.item3 -= 5
			equipment_to_delete.save()
			gorilla_to_buff.strength += 1
			gorilla_to_buff.save()
			messages.success(request, f"Your Gorilla started training")
			return redirect(train_gorilla)
		else:
			messages.error(request, f"You don't have enough resources to train your Gorilla")
			return redirect(train_gorilla)

def buff_gorilla_hp(request):
	current_user = request.user
	gorilla_to_buff = Gorilla.objects.all().get(owner=current_user)
	equipment_to_delete = Equipment.objects.all().get(equipment_owner=current_user)
	try:
		training_timer = TrainingTimer.objects.all().get(trained_gorilla=gorilla_to_buff)
		if training_timer:
			messages.error(request, f"Your Gorilla is already training!")
			return redirect(train_gorilla)
	except:
		if equipment_to_delete.item2 >= 1 and equipment_to_delete.item4 >=3 and equipment_to_delete.item5 >=2:
			new_timer = TrainingTimer(trained_gorilla=gorilla_to_buff)
			new_timer.save()
			equipment_to_delete.item2 -= 1
			equipment_to_delete.item4 -= 3
			equipment_to_delete.item5 -= 2
			equipment_to_delete.save()
			gorilla_to_buff.hp += 4
			gorilla_to_buff.save()
			messages.success(request, f"Your Gorilla started training")
			return redirect(train_gorilla)
		else:
			messages.error(request, f"You don't have enough resources to train your Gorilla")
			return redirect(train_gorilla)

def auction_house(request):
	current_user = request.user
	items = Equipment.objects.all().get(equipment_owner=current_user)
	my_auctions = None
	try:
		my_auctions = Auction.objects.all().filter(creator=current_user)
	except:
		pass
	try:
		auctions = Auction.objects.all()
	except:
		pass
	if request.method == "POST":
		new_auction = Auction(item=request.POST.get('items'),
								amount_of_items=request.POST.get('item_amount'),
								cost=int(request.POST.get('item_price'))*int(request.POST.get('item_amount')),
								creator=request.user)
		new_auction.save()
		item_to_remove = Equipment.objects.all().get(equipment_owner=request.user)
		item = request.POST.get('items')
		if item == "item1":
			item_to_remove.item1 -= int(request.POST.get('item_amount'))
		if item == "item2":
			item_to_remove.item2 -= int(request.POST.get('item_amount'))
		if item == "item3":
			item_to_remove.item3 -= int(request.POST.get('item_amount'))
		if item == "item4":
			item_to_remove.item4 -= int(request.POST.get('item_amount'))
		if item == "item5":
			item_to_remove.item5 -= int(request.POST.get('item_amount'))
		item_to_remove.save()
		messages.success(request, f"You successfully created an auction")
		return redirect(auction_house)

	return render(request, 'menupages/auctions.html', context={'items': items, 
							'auctions': auctions, 
							'my_auctions': my_auctions,
							'current_user': current_user})

def buy_item(request, pk, amount):
	auction = Auction.objects.all().get(id=pk)
	auction.amount_of_items = amount
	equipment = Equipment.objects.all().get(equipment_owner=request.user)
	seller_equipment = Equipment.objects.all().get(equipment_owner=auction.creator)
	if equipment.gold >= auction.cost:
		if auction.item == 'item1':
			equipment.item1 += auction.amount_of_items
			equipment.gold -= auction.cost
			equipment.save()
			seller_equipment.gold += auction.cost
			seller_equipment.save()
			auction.delete()
			messages.success(request, 'Udało się zakupić przedmioty!')
			return redirect(auction_house)
		elif auction.item == 'item2':
			equipment.item2 += auction.amount_of_items
			equipment.gold -= auction.cost
			equipment.save()
			seller_equipment.gold += auction.cost
			seller_equipment.save()
			auction.delete()
			messages.success(request, 'Udało się zakupić przedmioty!')
			return redirect(auction_house)
		elif auction.item == 'item3':
			equipment.item3 += auction.amount_of_items
			equipment.gold -= auction.cost
			equipment.save()
			seller_equipment.gold += auction.cost
			seller_equipment.save()
			auction.delete()
			messages.success(request, 'Udało się zakupić przedmioty!')
			return redirect(auction_house)
		elif auction.item == 'item4':
			equipment.item4 += auction.amount_of_items
			equipment.gold -= auction.cost
			equipment.save()
			seller_equipment.gold += auction.cost
			seller_equipment.save()
			auction.delete()
			messages.success(request, 'Udało się zakupić przedmioty!')
			return redirect(auction_house)
		elif auction.item == 'item5':
			equipment.item5 += auction.amount_of_items
			equipment.gold -= auction.cost
			equipment.save()
			seller_equipment.gold += auction.cost
			seller_equipment.save()
			auction.delete()
			messages.success(request, 'Udało się zakupić przedmioty!')
			return redirect(auction_house)
	else:
		messages.error(request, 'Nie posiadasz wystarczająco złota żeby kupić ten przedmiot')
		return redirect(auction_house)

def cancel_auction(request, itemname, pk):
	my_auction = Auction.objects.all().get(id=pk)
	my_auction.item = itemname
	my_equipment = Equipment.objects.all().get(equipment_owner=request.user)
	if my_auction.item == 'item1':
		my_equipment.item1 += my_auction.amount_of_items
		my_equipment.save()
		my_auction.delete()
		messages.success(request, 'Anulowano aukcje')
		return redirect(auction_house)
	elif my_auction.item == 'item2':
		my_equipment.item2 += my_auction.amount_of_items
		my_equipment.save()
		my_auction.delete()
		messages.success(request, 'Anulowano aukcje')
		return redirect(auction_house)
	elif my_auction.item == 'item3':
		my_equipment.item3 += my_auction.amount_of_items
		my_equipment.save()
		my_auction.delete()
		messages.success(request, 'Anulowano aukcje')
		return redirect(auction_house)
	elif my_auction.item == 'item4':
		my_equipment.item4 += my_auction.amount_of_items
		my_equipment.save()
		my_auction.delete()
		messages.success(request, 'Anulowano aukcje')
		return redirect(auction_house)
	elif my_auction.item == 'item5':
		my_equipment.item5 += my_auction.amount_of_items
		my_equipment.save()
		my_auction.delete()
		messages.success(request, 'Anulowano aukcje')
		return redirect(auction_house)

def gorilla_options(request):
	all_owned_gorillas = Gorilla.objects.all().filter(owner=request.user)
	context = {
		'all_owned_gorillas': all_owned_gorillas
	}

	return render(request, 'menupages/gorilla_options.html' , context)

def feed_gorilla(request):
	gorilla = Gorilla.objects.all().get(owner=request.user)
	if request.method == "POST":
		if gorilla.feeding + timedelta(hours=24)<= datetime.date(timezone.now()):
			gorilla.level += 1
			gorilla.strength += 1
			gorilla.hp += 4
			gorilla.feeding = timezone.now()
			if gorilla.level >= 6:
				gorilla.look = 'gorilla650.png'
			gorilla.save()
			messages.success(request, f"{gorilla.name} został nakarmiony!\nJego statystyki wzrosły!")
			return redirect(feed_gorilla)
		elif gorilla.feeding + timedelta(hours=24) > datetime.date(timezone.now()):
			messages.error(request, f"{gorilla.name} nie jest jeszcze głodny!")
			return redirect(feed_gorilla)
	context = {
		'gorilla': gorilla
	}
	return render(request, 'menupages/feed_gorilla.html', context=context)

def show_stats(request):
	gorilla = Gorilla.objects.all().get(owner=request.user)
	context = {
		'gorilla': gorilla
	}

	return render(request, 'menupages/stats.html', context=context)

def user_profile(request, pk):
	profile_to_view = User.objects.all().get(id=pk)
	user_gorilla = Gorilla.objects.all().get(owner=profile_to_view)
	user_equipment = Equipment.objects.all().get(equipment_owner=profile_to_view)
	profile_text = Profile.objects.all().get(owner=profile_to_view)
	context = {
		"profile_to_view": profile_to_view,
		"user_gorilla": user_gorilla,
		"user_equipment": user_equipment,
		"profile_text": profile_text
	}
	return render(request, "menupages/user_profile.html", context=context)

def edit_profile(request):
	user_profile = Profile.objects.all().get(owner=request.user)
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=user_profile)
		if profile_form.is_valid():
			user_profile = profile_form.save(commit=False)
			user_profile.owner = request.user
			user_profile.save()
			messages.success(request, f"Zaktualizowano profil!")
			return redirect(gorilla_options)
	else:
		profile_form = ProfileForm

	return render(request, 'menupages/edit_profile.html', {'form': profile_form})

def buy_bananas(request):
	currency = Equipment.objects.all().get(equipment_owner=request.user)
	context = {
		'currency': currency
	}
	return render(request, 'menupages/buy_bananas.html', context=context)

def letters(request):
	try:
		letters = Letter.objects.all().filter(receiver=request.user)
	except:
		letters = None
	
	context = {
		'letters': letters
	}
	return render(request, 'menupages/letters.html', context=context)

def send_letter(request):
	if request.method == 'POST':
		letter_form = LetterForm(request.POST)
		if letter_form.is_valid():
			new_letter = letter_form.save(commit=False)
			new_letter.sender = request.user
			new_letter.save()
			messages.success(request, f"Wysłano list!")
			return redirect(letters)
		else:
			messages.error(request, f"Wystąpił błąd!")
			return redirect(letters)
	else:
		letter_form = LetterForm

	return render(request, 'menupages/send.html', {'form': letter_form})

def letter_content(request, pk):
	letter_to_view = Letter.objects.all().get(id=pk)
	context = {
		'letter_to_view': letter_to_view
	}

	return render(request, 'menupages/view_letter.html', context=context)
