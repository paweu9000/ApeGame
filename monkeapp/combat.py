from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Gorilla, Equipment, Opponent, TrainingTimer
from random import choice
import json

def pve_combat(request):
	current_user = request.user
	my_gorillas = Gorilla.objects.all().get(owner=current_user)
	new_opponent = Opponent.objects.all()
	context = {
		'my_gorillas': my_gorillas,
		'new_opponent': new_opponent
	}
	return render(request, 'combat/pve_combat.html', context=context)

def combat(request, pk):
	enemy = Opponent.objects.all().get(id=pk)
	equipment = Equipment.objects.all().get(equipment_owner=request.user)
	my_gorilla = Gorilla.objects.all().get(owner=request.user)
	move_list = []
	gorilla_hp_list = []
	enemy_hp_list = []
	x = my_gorilla.strength
	y = enemy.strength
	gorilla_hp = my_gorilla.hp
	enemy_hp = enemy.health_points
	winner: str
	items_to_win = [1, 2, 3, 4, 5]
	prize: str
	to_win = choice(items_to_win)
	try:
		if TrainingTimer.objects.all().get(trained_gorilla=my_gorilla):
			messages.error(request, f"Your Gorilla cannot fight while he is training!")
			return redirect(pve_combat)
	except:
		pass
	
	while gorilla_hp > 0 and enemy_hp > 0:
		move_list.append(f"{enemy.name} uderza {my_gorilla.name} za {str(y)} obrazen")
		gorilla_hp_list.append(gorilla_hp)
		gorilla_hp -= y
		if gorilla_hp_list[:-1] != gorilla_hp:
			gorilla_hp_list.append(gorilla_hp)
		move_list.append(f"{my_gorilla.name} uderza {enemy.name} za {str(x)} obrazen")
		enemy_hp_list.append(enemy_hp)
		enemy_hp -= x
		if enemy_hp_list[:-1] != enemy_hp:
			enemy_hp_list.append(enemy_hp)
		if gorilla_hp > 0 and enemy_hp <= 0:
			winner = f"{my_gorilla.name} zwycięża!"
			move_list.append(winner)
			if to_win == 1:
				equipment.item1 += 1
				prize = f"{my_gorilla.name} zdobył 1 Banan!"
				move_list.append(prize)
			elif to_win == 2:
				equipment.item2 += 1
				prize = f"{my_gorilla.name} zdobył 1 Smoczy owoc!"
				move_list.append(prize)
			elif to_win == 3:
				equipment.item3 += 1
				prize = f"{my_gorilla.name} zdobył 1 Szpinak!"
				move_list.append(prize)
			elif to_win == 4:
				equipment.item4 += 1
				prize = f"{my_gorilla.name} zdobył 1 Jabłko!"
				move_list.append(prize)
			elif to_win == 5:
				equipment.item5 += 1
				prize = f"{my_gorilla.name} zdobył 1 Sałata!"
				move_list.append(prize)
			equipment.save()
		elif gorilla_hp < 0 and enemy_hp > 0:
			winner = f"{enemy.name} pokonuje {my_gorilla.name}!"
			move_list.append(winner)
			prize = None
	#gorilla_hp_list = json.dumps(gorilla_hp_list)
	context = {
		'enemy': enemy,
		'my_gorilla': my_gorilla,
		'move_list': json.dumps(move_list),
		'gorilla_hp_list': gorilla_hp_list,
		'enemy_hp_list': enemy_hp_list
	}
	return render(request, 'combat/combat.html', context=context)

def pvp_gorillas(request):
	all_gorillas = None
	try:
		all_gorillas = Gorilla.objects.all().exclude(owner=request.user)
		context = {
			'all_gorillas': all_gorillas
		}
	except:
		pass
	return render(request, 'combat/pvp_gorillas.html', context)

def pvp_combat(request, pk):
	enemy_gorilla = Gorilla.objects.all().get(id=pk)
	equipment = Equipment.objects.all().get(equipment_owner=request.user)
	my_gorilla = Gorilla.objects.all().get(owner=request.user)
	move_list = []
	gorilla_hp_list = []
	enemy_gorilla_hp_list = []
	x = my_gorilla.strength
	y = enemy_gorilla.strength
	gorilla_hp = my_gorilla.hp
	enemy_hp = enemy_gorilla.hp
	winner: str
	prize: str
	try:
		if TrainingTimer.objects.all().get(trained_gorilla=my_gorilla):
			messages.error(request, f"Your Gorilla cannot fight while he is training!")
			return redirect(pvp_gorillas)
	except:
		pass
	
	while gorilla_hp > 0 and enemy_hp > 0:
		move_list.append(f"{enemy_gorilla.name} uderza {my_gorilla.name} za {str(y)} obrazen")
		gorilla_hp_list.append(gorilla_hp)
		gorilla_hp -= y
		if gorilla_hp_list[:-1] != gorilla_hp:
			gorilla_hp_list.append(gorilla_hp)	
		move_list.append(f"{my_gorilla.name} uderza {enemy_gorilla.name} za {str(x)} obrazen")
		enemy_gorilla_hp_list.append(enemy_hp)
		enemy_hp -= x
		if enemy_gorilla_hp_list[:-1] != enemy_hp:
			enemy_gorilla_hp_list.append(enemy_hp)
		if gorilla_hp > 0 and enemy_hp <= 0:
			winner = f"{my_gorilla.name} zwycięża!"
			move_list.append(winner)
			equipment.gold += my_gorilla.level + enemy_gorilla.level + 10
			equipment.save()
			my_gorilla.pvp_points += my_gorilla.level + enemy_gorilla.level + 5
			my_gorilla.save()
			prize = f"{my_gorilla.name} zdobywa {(my_gorilla.level + enemy_gorilla.level + 10)} złota!"
			move_list.append(prize)
		elif gorilla_hp < 0 and enemy_hp > 0:
			winner = f"{enemy_gorilla.name} pokonuje {my_gorilla.name}!"
			move_list.append(winner)
			prize = None
	move_list = json.dumps(move_list)
	#gorilla_hp_list = json.dumps(gorilla_hp_list)
	context = {
		'enemy_gorilla': enemy_gorilla,
		'my_gorilla': my_gorilla,
		'move_list': move_list,
		'gorilla_hp_list': gorilla_hp_list,
		'enemy_gorilla_hp_list': enemy_gorilla_hp_list
	}
	print(move_list)
	return render(request, 'combat/pvpcombat.html', context=context)