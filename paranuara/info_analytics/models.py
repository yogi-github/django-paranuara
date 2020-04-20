from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'companies'
        app_label = 'info_analytics'

    def __str__(self):
        return self.name


class Food(models.Model):

    FRUITS = 'F'
    VEGETABLES = 'V'

    FOOD_CHOICES = (
        (FRUITS, 'F'),
        (VEGETABLES, 'V'),
    )

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=1, choices=FOOD_CHOICES)

    class Meta:
        db_table = 'food'
        app_label = 'info_analytics'

    def __str__(self):
        return self.name


class Person(models.Model):

    guid = models.CharField(max_length=255, unique=True)
    has_died = models.BooleanField(default=False)
    balance = models.CharField(max_length=100, default='0')
    picture = models.CharField(max_length=500, blank=True)
    age = models.IntegerField()
    eye_color = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=500)
    about = models.TextField(blank=True)
    registered = models.DateTimeField()
    tags = models.TextField(blank=True)
    greeting = models.TextField(blank=True)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True, related_name='company')
    favourite_food = models.ManyToManyField(Food, related_name='food', db_table='people_food', blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, db_table='people_friends', blank=True)

    class Meta:
        db_table = 'people'
        app_label = 'info_analytics'

    def __str__(self):
        return self.email
