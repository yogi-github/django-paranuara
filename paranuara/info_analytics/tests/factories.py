import datetime
import string

import factory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyInteger, FuzzyDateTime
from pytz import UTC

from info_analytics.models import Company, Food, Person


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: "Company{}".format(n))


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    name = factory.Sequence(lambda n: "Food{}".format(n))
    type = FuzzyChoice(Food.FOOD_CHOICES)


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    guid = FuzzyText(length=10, chars=string.ascii_lowercase + string.digits)
    age = FuzzyInteger(21, 99)
    eye_color = 'brown'
    name = factory.Sequence(lambda n: "User{}".format(n))
    gender = 'Male'
    phone = factory.Sequence(lambda n: '0486-992-%03d' % n)
    email = factory.LazyAttribute(lambda obj: u'{}@test.com'.format(obj.name).lower())
    address = factory.Faker('address')
    registered = FuzzyDateTime(datetime.datetime(2020, 1, 1, tzinfo=UTC))
    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def favourite_food(self, create, extracted, **kwargs):
        if not create:
            # simple build, do nothing
            return

        if extracted:
            for food in extracted:
                self.favourite_food.add(food)

    @factory.post_generation
    def friends(self, create, extracted, **kwargs):
        if not create:
            # simple build, do nothing
            return

        if extracted:
            for friend in extracted:
                self.friends.add(friend)
