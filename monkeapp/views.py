from django.shortcuts import render
from .models import Gorilla, Equipment



# Create your views here.


def homepage(request):
	if not request.user.is_authenticated:
		return render(request, 'menupages/homepage.html')
	else:
		current_user = request.user
		try:
			gorillas = Gorilla.objects.all().get(owner=current_user.id)
			money = Equipment.objects.all().get(equipment_owner=request.user)
			all_gorillas = Gorilla.objects.all().order_by('-pvp_points')[:40]
			context = {
				'gorillas': gorillas,
				'money': money,
				'all_gorillas': all_gorillas
			}
			return render(request, 'menupages/homepage.html', context=context)
		except:
			gorillas = None
			return render(request, 'menupages/homepage.html', context=gorillas)


def gorilla_windows(request, pk):
	gorilla_to_view = Gorilla.objects.all().get(id=pk)
	context = {
		'gorilla_to_view': gorilla_to_view
	}
	return render(request, 'popup/popupmonkey.html', context=context)

def gorilla_windows_pvp(request, pk):
	gorilla_to_view = Gorilla.objects.all().get(id=pk)
	context = {
		'gorilla_to_view': gorilla_to_view
	}
	return render(request, 'popup/popuppvp.html', context=context)


