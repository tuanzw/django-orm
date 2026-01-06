from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    user = User.objects.last()
    restaurant = Restaurant.objects.last()
    
    rating = Rating(
        restaurant=restaurant,
        user=user,
        rating=9
    )

    # rating.full_clean() # model validation is not run on save by default
    rating.save()

    pprint(connection.queries)
