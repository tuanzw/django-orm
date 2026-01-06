from django.forms import ModelForm
from core.models import Rating

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['restaurant', 'user', 'rating']