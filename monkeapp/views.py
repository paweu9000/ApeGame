from django.shortcuts import render, redirect
from .forms import RegisterForm, GorillaForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Gorilla, Equipment, Opponent
from random import choice


# Create your views here.

def homepage(request):
	if not request.user.is_authenticated:
		return render(request, 'homepage.html')
	else:
		current_user = request.user
		try:
			gorillas = Gorilla.objects.all().get(owner=current_user.id)
			context = {
				'gorillas': gorillas
			}
			return render(request, 'homepage.html', context=context)
		except:
			gorillas = None
			return render(request, 'homepage.html', context=gorillas)

def register_page(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			Equipment.objects.create(equipment_owner=new_user)
			messages.success(request, f"Rejestracja przebiegła pomyślnie\nZaloguj się!")
			return redirect(login_page)
	else:
		form = RegisterForm

	return render(request, 'register.html', {'form': form})

def login_page(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect(homepage)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect(homepage)

def get_gorilla(request):
	if not request.user.is_authenticated:
		return redirect(homepage)
	if request.method == "POST":
		form = GorillaForm(request.POST)
		if form.is_valid():
			new_Gorilla = Gorilla(name=form.cleaned_data.get('name'))
			new_Gorilla.owner = request.user
			new_Gorilla.save()
			messages.success(request, f"You have just adopted gorilla!")
			return redirect(homepage)
		else: 
			messages.error(request, "Something went wrong")
	form = GorillaForm()
	return render(request, 'get_gorilla.html', context={"gorilla_form":form})

def equipment(request):
	if not request.user.is_authenticated:
		return redirect(homepage)
	items = Equipment.objects.all().get(equipment_owner=request.user.id)
	context = {
		'items': items
	}
	return render(request, 'equipment.html', context=context)

def train_gorilla(request):
	current_user = request.user
	all_gorillas = Gorilla.objects.all().get(owner=current_user)
	items = Equipment.objects.all().get(equipment_owner=request.user)
	context = {
		'all_gorillas': all_gorillas,
		'items': items
	}
	
	return render(request, 'training.html', context=context)

def buff_gorilla(request):
	current_user = request.user
	gorilla_to_buff = Gorilla.objects.all().get(owner=current_user)
	equipment_to_delete = Equipment.objects.all().get(equipment_owner=current_user)
	if equipment_to_delete.item1 >= 2 and equipment_to_delete.item3 >=5:
		equipment_to_delete.item1 -= 2
		equipment_to_delete.item3 -= 5
		equipment_to_delete.save()
		gorilla_to_buff.strength += 1
		gorilla_to_buff.save()
		messages.success(request, f"Your Gorilla just got stronger")
		return redirect(train_gorilla)
	else:
		messages.error(request, f"You don't have enough resources to train your Gorilla")
		return redirect(train_gorilla)

def pve_combat(request):
	current_user = request.user
	my_gorilla = Gorilla.objects.all().get(owner=current_user)
	new_opponent = Opponent.objects.all()
	context = {
		'my_gorilla': my_gorilla,
		'new_opponent': new_opponent
	}
	return render(request, 'pve_combat.html', context=context)

def combat(request, pk):
	enemy = Opponent.objects.all().get(id=pk)
	equipment = Equipment.objects.all().get(equipment_owner=request.user)
	my_gorilla = Gorilla.objects.all().get(owner=request.user)
	move_list = []
	x = my_gorilla.strength
	y = enemy.strength
	gorilla_hp = my_gorilla.hp
	enemy_hp = enemy.health_points
	winner: str
	items_to_win = [1, 2, 3, 4, 5]
	prize: str
	to_win = choice(items_to_win)
	
	while gorilla_hp > 0 and enemy_hp > 0:
		move_list.append(f"{enemy.name} uderza {my_gorilla.name} za {str(y)} obrażeń")
		gorilla_hp -= y
		move_list.append(f"{my_gorilla.name} uderza {enemy.name} za {str(x)} obrażeń")
		enemy_hp -= x
		if gorilla_hp > 0 and enemy_hp <= 0:
			winner = f"{my_gorilla.name} zwycięża!"
			if to_win == 1:
				equipment.item1 += 1
				prize = f"{my_gorilla.name} zdobył 1 Banan!"
			elif to_win == 2:
				equipment.item2 += 1
				prize = f"{my_gorilla.name} zdobył 1 Smoczy owoc!"
			elif to_win == 3:
				equipment.item3 += 1
				prize = f"{my_gorilla.name} zdobył 1 Szpinak!"
			elif to_win == 4:
				equipment.item4 += 1
				prize = f"{my_gorilla.name} zdobył 1 Jabłko!"
			elif to_win == 5:
				equipment.item5 += 1
				prize = f"{my_gorilla.name} zdobył 1 Sałata!"
			equipment.save()
		else:
			winner = f"{enemy.name} pokonuje {my_gorilla.name}!"
			prize = None
	context = {
		'enemy': enemy,
		'my_gorilla': my_gorilla,
		'move_list': move_list,
		'winner': winner,
		'prize': prize
	}
	return render(request, 'combat.html', context=context)

def pvp_gorillas(request):
	all_gorillas = Gorilla.objects.all()
	context = {
		'all_gorillas': all_gorillas
	}
	return render(request, 'pvp_gorillas.html', context)
