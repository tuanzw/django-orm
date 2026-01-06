from django.shortcuts import render
from .forms import RatingForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'index.html', {'form': form})
    context = {'form': RatingForm()}
    return render(request, 'index.html', context)