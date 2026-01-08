from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection
from django.db.models.functions import Lower

from pprint import pprint

def run():
    # filter restaurants that have rating is greater than or equal to 3
    restaurants = Restaurant.objects.filter(ratings__rating__gte=3)
    print(restaurants)
    pprint(connection.queries)
