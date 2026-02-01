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

## 03. Model Field Validators/Custom Validators
>https://docs.djangoproject.com/en/6.0/ref/validators/  
>validators will not be run automatically when you save a model
>https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/#validation-on-a-modelform
>https://docs.djangoproject.com/en/6.0/ref/models/instances/#validating-objects  
>When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form  
>You should only need to call a **model’s full_clean()** method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation.

Add MinValueValidator, MaxValueValidator to Rating model  
```
from django.core.validators import MinValueValidator, MaxValueValidator
.....
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
```  
```
def run():
    user = User.objects.last()
    restaurant = Restaurant.objects.last()
    
    rating = Rating(
        restaurant=restaurant,
        user=user,
        rating=9
    )

    rating.full_clean() # model validation is not run on save by default
    rating.save()

    pprint(connection.queries)
```  

Using ModelForm & calling is_valid to perform the validators
Create forms.py under app folder  
```
from django.forms import ModelForm
from core.models import Rating

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['restaurant', 'user', 'rating']
```  
Adding logic to handle the request to views.py  
```
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
```  
Create urls.py under app folder  
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```  
Create templates folder under app folder  
Create templates/base.html file  
```
{% load static %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django ORM Example</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
</head>

<body>
    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>
</body>

</html>
```  
Create templates/index.html file  
```{% extends 'base.html' %}

{% block content %}
<h1>Submit a Rating</h1>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary" type="submit">Submit</button>
</form>
{% endblock %}
```  
`pip install jinja2` for using Jinja template  

Adding url part of the app to the project urls.py  
```
    path('', include('core.urls')),
```  
Start server and the form will validate out of range of rating while submitting.  

Adding validation at database level  
```
from django.db.models import Q, CheckConstraint
.....

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(rating__gte=1) & Q(rating__lte=5),
                name='rating_range_1_and_5_check'
            )
        ]
```  
```
CREATE TABLE "core_rating" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), 
  "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
  "restaurant_id" bigint NOT NULL REFERENCES "core_restaurant" ("id") DEFERRABLE INITIALLY DEFERRED, 
  CONSTRAINT "rating_range_1_and_5_check" CHECK (
    (
      "rating" >= 1 
      AND "rating" <= 5
    )
  )
)
```  
>django.db.utils.IntegrityError: CHECK constraint failed: rating_range_1_and_5_check  
Validator can be at Model, ModelForm, database.  
Custom validator can be passed to validators field example validators=[check_something]

## 04. Update/Delete/on_delete behaviour/ Query Set querying & lookup  
### Update a record  
Example
```
    restaurant.name = "New name"
    restaurant.save()
```  
```
 [{'sql': 'UPDATE "core_restaurant" SET "name" = \'New Indian restaurant\', '
         '"website" = \'\', "date_opened" = \'2026-01-08\', "latitude" = 37.4, '
         '"longitude" = 122.1, "restaurant_type" = \'IN\' WHERE '
         '"core_restaurant"."id" = 2',
  'time': '0.030'}]
```  
Checking if model is updated: https://docs.djangoproject.com/en/6.0/ref/models/instances/#state  
The ModelState object has two attributes: adding, a flag which is True if the model has not been saved to the database yet, and db, a string referring to the database alias the 
instance was loaded from or saved to.  
Adding custome save() in Restaurant model
```
    def save(self, *args, **kwargs):
        print(self._state.adding)
        super().save(*args, **kwargs)

```  
Model signals: https://docs.djangoproject.com/en/6.0/ref/signals/  
### Update records (queryset) 
https://docs.djangoproject.com/en/6.0/topics/db/queries/#updating-multiple-objects-at-once  
```
    restaurants = Restaurant.objects.all()
    restaurants.update(website='https://www.example.com')
```  
```
[{'sql': 'UPDATE "core_restaurant" SET "website" = \'https://www.example.com\'',
  'time': '0.034'}]
```  
Be aware that the update() method is converted directly to an SQL statement. It is a bulk operation for direct updates. It doesn’t run any save() methods on your models, or emit the pre_save or post_save signals (which are a consequence of calling save()), or honor the auto_now field option. If you want to save every item in a QuerySet and make sure that the save() method is called on each instance, you don’t need any special function to handle that. Loop over them and call save():  
```
    for restaurant in restaurants:
        restaurant.save()
```  
```
def run():
    restaurants = Restaurant.objects.filter(name__startswith='P')
    restaurants.update(
        website='https://www.pizza-shop.com',
        date_opened=timezone.now() - timezone.timedelta(days=365))

    pprint(connection.queries)
```  
```
[{'sql': 'UPDATE "core_restaurant" SET "website" = '
         '\'https://www.pizza-shop.com\', "date_opened" = \'2025-01-08\' WHERE '
         '"core_restaurant"."name" LIKE \'P%\' ESCAPE \'\\\'',
  'time': '0.010'}]
```  
-> only 1 update statment as django is lazy loading.  

### Delete  
https://docs.djangoproject.com/en/6.0/topics/db/queries/#deleting-objects  
The delete method, conveniently, is named delete(). This method immediately deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type  
```
    restaurant = Restaurant.object.first()
    restaurant.delete()
```  
You can also delete objects in bulk. Every QuerySet has a delete() method, which deletes all members of that QuerySet.
Keep in mind that this will, whenever possible, be executed purely in SQL, and so the delete() methods of individual object instances will not necessarily be called during the process.  
```
    restaurants = Restaurant.object.all()
    restaurants.delete()
```    
### on_delete behaviour  
### Copying model instance  
https://docs.djangoproject.com/en/6.0/topics/db/queries/#deleting-objects  
set the pk to None & set _state.adding to True  
This process doesn’t copy relations that aren’t part of the model’s database table  
```
def run():
    restaurant = Restaurant.objects.last()
    print(restaurant)

    restaurant.pk = None
    restaurant._state.adding = True
    restaurant.save()

    pprint(connection.queries)
```  
```
New Indian restaurant2
True
[{'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitude", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" ORDER BY '
         '"core_restaurant"."id" DESC LIMIT 1',
  'time': '0.000'},
 {'sql': 'INSERT INTO "core_restaurant" ("name", "website", "date_opened", '
         '"latitude", "longitude", "restaurant_type") VALUES (\'New Indian '
         "restaurant2', 'https://www.example.com', '2026-01-08', 37.4, 122.1, "
         '\'IN\') RETURNING "core_restaurant"."id"',
  'time': '0.003'}]
```  
### Lookup  
https://docs.djangoproject.com/en/6.0/topics/db/queries/#field-lookups  
https://docs.djangoproject.com/en/6.0/topics/db/queries/#key-index-and-path-transforms  
Filtering records with filter() mehtod  
```
    restaurants = Restaurant.objects.filter(restaurant_type=Restaurant.TypeChoices.CHINESE, \
        name__contains='c')
```  
```
[{'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitude", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" WHERE '
         '("core_restaurant"."name" LIKE \'%c%\' ESCAPE \'\\\' AND '
         '"core_restaurant"."restaurant_type" = \'CH\') LIMIT 21',
  'time': '0.000'}]
```  
```
    restaurants = Restaurant.objects.filter(restaurant_type__in=[
        Restaurant.TypeChoices.ITALIAN,
        Restaurant.TypeChoices.CHINESE,
        Restaurant.TypeChoices.INDIAN
    ])
```  
get() to return single instance, error if there is more than 1 records  
```
    restaurant = Restaurant.objects.get(pk=4)
```  
exists()  
exclude()  
```
    restaurants = Restaurant.objects.exclude(restaurant_type__in=[
        Restaurant.TypeChoices.ITALIAN,
        Restaurant.TypeChoices.CHINESE,
        Restaurant.TypeChoices.INDIAN
    ])
```  
```
[{'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitude", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" WHERE NOT '
         '("core_restaurant"."restaurant_type" IN (\'IT\', \'CH\', \'IN\')) '
         'LIMIT 21',
  'time': '0.000'}]
```  
Filtering QuerySets with lt & gt & lte & gte, range, 
-> Model.objects.filter(fieldname1__lt=value, fieldname2__gt=value)  
order_by()  
-> Model.object.filter(....).order_by('fieldname')  (for asc)  
-> Model.object.filter(....).order_by('-fieldname')  (for desc) 
```
    restaurants = Restaurant.objects.filter(restaurant_type=Restaurant.TypeChoices.MEXICAN) \
        .order_by(Lower('name'))
```  
Can setup ordering in Meta class of a model  
```
    class Meta:
        ordering = [Lower('name')]
```   
Filtering by Foreign Key  
filter restaurants that have rating is greater than or equal to 3  
```
    restaurants = Restaurant.objects.filter(ratings__rating__gte=3)
```  
```
[{'sql': 'SELECT "core_restaurant"."id", "core_restaurant"."name", '
         '"core_restaurant"."website", "core_restaurant"."date_opened", '
         '"core_restaurant"."latitude", "core_restaurant"."longitude", '
         '"core_restaurant"."restaurant_type" FROM "core_restaurant" INNER '
         'JOIN "core_rating" ON ("core_restaurant"."id" = '
         '"core_rating"."restaurant_id") WHERE "core_rating"."rating" >= 3 '
         'ORDER BY LOWER("core_restaurant"."name") ASC LIMIT 21',
  'time': '0.000'}]
```  
## 05. N+1 Problem - select_related & prefetch_related  
django-debug-toolbar https://django-debug-toolbar.readthedocs.io/en/latest/installation.html  
`pip install django-debug-toolbar`  
```
INSTALLED_APPS = [
    .....
    'debug_toolbar',
]
```
Add urls  
```
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    .....
] + debug_toolbar_urls()
```  
Add middleware  
```
MIDDLEWARE = [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]
```  
Internal IPs end of project setting  
```
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
```  
https://docs.djangoproject.com/en/6.0/howto/static-files/#serving-static-files-during-development  
-> no need  
Start the server & will see debug toolbar on the right hand side of the page  
select_related https://docs.djangoproject.com/en/6.0/ref/models/querysets/#prefetch-related  
prefetch_related https://docs.djangoproject.com/en/6.0/ref/models/querysets/#prefetch-related  
select_related works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query. However, to avoid the much larger result set that would result from joining across a ‘many’ relationship, select_related is limited to single-valued relationships - foreign key and one-to-one.  
prefetch_related, on the other hand, does a separate lookup for each relationship, and does the ‘joining’ in Python. This allows it to prefetch many-to-many, many-to-one, and GenericRelation objects which cannot be done using select_related, in addition to the foreign key and one-to-one relationships that are supported by select_related. It also supports prefetching of GenericForeignKey, however, the queryset for each ContentType must be provided in the querysets parameter of GenericPrefetch.  
```
    restaurants = Restaurant.objects.prefetch_related('ratings')
```  






