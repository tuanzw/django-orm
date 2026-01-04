# django-orm
Django ORM

## 01. To start from scratch, clone the project at main branch
Open cmd  
`cd \django-orm`  
`python -m venv venv`  
`venv\Scripts\activate`  
`pip install -r requirements.txt`  
`django-admin startproject orm_series .`  
`python maange.py startapp core`  

Adding app to **INSTALLED_APPS**
```
INSTALLED_APPS = [
    ...,
    'django_extensions',
    'core',
]
```  

Create models (Restaurant, Rating, Sale)
```
class Restaurant(models.Model):
    class TypeChoices(models.TextChoices):
        INDIAN = 'IN', 'Indian'
        CHINESE = 'CH', 'Chinese'
        ITALIAN = 'IT', 'Italian'
        GREEK = 'GR', 'Greek'
        MEXICAN = 'MX', 'Mexican'
        FASTFOOD = 'FF', 'Fast Food'
        OTHER = 'OT', 'Other'

    name = models.CharField(max_length=100)
    website = models.URLField(default='')
    date_opened = models.DateField()
    latitude = models.FloatField()
    longitue = models.FloatField()
    restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.OTHER)

    def __str__(self):
        return self.name
    

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Rating: {self.rating}"
    

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()
```  

Register models to admin sites - file admin.py
```
from core.models import Restaurant, Rating, Sale

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Rating)
admin.site.register(Sale)
```  
Migrations  
`python manage.py makemigrations`  
`python manage.py migrate`  

Create superuse
`python manage.py createsuperuse`  

## 02. Querying and Creating Records
Open cmd and go to project root directory
`mkdir scripts`  
`echo. > scripts/__init__.py`  
`echo. > scripts/orm_script.py`  
To run the script  
`python manage.py runscript orm_script` 
Using save() method to create a record to database
```
from core.models import Restaurant, Rating, Sale
from django.utils import timezone

def run():
    restaurant = Restaurant()
    restaurant.name = "My Italian restaurant"
    restaurant.latitude = 50.2
    restaurant.longitue = 50.2
    restaurant.date_opened = timezone.now()
    restaurant.restaurant_type = Restaurant.TypeChoices.ITALIAN

    restaurant.save()
```  
In Django, Lazy loading is the default behavior of the ORM
```
from django.db import connection

from pprint import pprint

def run():
    restaurant = Restaurant.objects.all()
    print(restaurant) # comment out then no queries

    pprint(connection.queries)
```  
```
<QuerySet [<Restaurant: My Italian restaurant>]>
[{'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitue", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" LIMIT 21',
  'time': '0.000'}]
  ```  
Django shell plus  
`python manage.py shell_plus --print-sql`  
`>>> Restaurant.objects.all()`  

create() method
```
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    restaurant = Restaurant.objects.create(
        name="Pizza Shop",
        date_opened = timezone.now(),
        restaurant_type = Restaurant.TypeChoices.ITALIAN,
        latitude = 50.2,
        longitude = 50.2
    )

    pprint(connection.queries)
```  
Many to many Rating creation
```
from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    restaurant = Restaurant.objects.first()
    user = User.objects.first()
    rating = Rating.objects.create(user=user, restaurant=restaurant, rating=3)

    print(rating)
    pprint(connection.queries)
```  
Querying the many to many table
```
from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    rating = Rating.objects.first()
    print(rating.restaurant)    
    pprint(connection.queries)
```  
2 queries - rating & restaurant
```
My Italian restaurant
[{'sql': 'SELECT "core_rating"."id", "core_rating"."restaurant_id", '
         '"core_rating"."user_id", "core_rating"."rating" FROM "core_rating" '
         'ORDER BY "core_rating"."id" ASC LIMIT 1',
  'time': '0.000'},
 {'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitude", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" WHERE '
         '"core_restaurant"."id" = 1 LIMIT 21',
  'time': '0.000'}]
```  

Customer reverse manager  
***related_name="ratings"***    
```
restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="ratings")
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
```  
```
from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    restaurant = Restaurant.objects.first()

    print(restaurant.ratings.all())
      
    pprint(connection.queries)
```  
get_or_create()  
```
from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

from pprint import pprint

def run():
    user = User.objects.first()
    restaurant = Restaurant.objects.first()
    
    rating, created = Rating.objects.get_or_create(
        restaurant=restaurant,
        user=user,
        rating=4
    )

    if created:
        print("Rating {rating} added!")
    pprint(connection.queries)
```  





