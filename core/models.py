from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, CheckConstraint
from django.db.models.functions import Lower

# Restaurant
# User
# Rating
# Sale

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
    longitude = models.FloatField()
    restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.OTHER)

    class Meta:
        ordering = [Lower('name')]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print(self._state.adding)
        super().save(*args, **kwargs)


class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        managed = True
        constraints = [
            CheckConstraint(
                condition=Q(rating__gte=1) & Q(rating__lte=5),
                name='rating_range_1_and_5_check'
            )
        ]

    def __str__(self):
        return f"Rating: {self.rating}"
    

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name="sales")
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()
    

