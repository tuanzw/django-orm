from django.shortcuts import render
from core.forms import RatingForm
from core.models import Restaurant

# Create your views here.
def index(request):
    # if request.method == 'POST':
    #     form = RatingForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     else:
    #         return render(request, 'index.html', {'form': form})
    # context = {'form': RatingForm()}
    # return render(request, 'index.html', context)
    # restaurants = Restaurant.objects.prefetch_related('ratings')
    restaurants = Restaurant.objects.filter(ratings__rating=3)
    # restaurants = Restaurant.objects.filter(ratings=3)
    context = {'restaurants': restaurants}
    return render(request, 'index.html', context)