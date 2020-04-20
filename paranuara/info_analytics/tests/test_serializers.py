from django.test import TestCase

from info_analytics.models import Food
from info_analytics.serializers import PeopleSerializer, PeoplePagedSerializer, CommonFriendsSerializer, \
    FavouriteFoodSerializer
from info_analytics.tests.factories import PersonFactory, CompanyFactory, FoodFactory
from info_analytics.view_models import PeopleViewModel, CommonFriendsViewModel, FavouriteFoodViewModel


class SerializerTestMixin(TestCase):

    def setUp(self):

        self.friend1 = PersonFactory(eye_color='brown', has_died=False)
        self.friend2 = PersonFactory(eye_color='brown', has_died=True)
        self.friend3 = PersonFactory(eye_color='black')
        self.friend4 = PersonFactory(eye_color='green')
        self.friend5 = PersonFactory(eye_color='blue')

        self.veggie = FoodFactory(type=Food.VEGETABLES)
        self.fruit = FoodFactory(type=Food.FRUITS)

        self.person1 = PersonFactory(
            friends=[self.friend1, self.friend2, self.friend3, self.friend4],
            favourite_food=[self.veggie, self.fruit]
        )
        self.person2 = PersonFactory(friends=[self.friend1, self.friend2, self.friend3, self.friend5])


class PeopleSerializerTestTest(SerializerTestMixin):

    def test_serializes(self):

        serializer = PeopleSerializer(self.person1)

        data = serializer.data
        self.assertEqual(data['id'], self.person1.id)
        self.assertEqual(data['name'], self.person1.name)
        self.assertEqual(data['age'], self.person1.age)
        self.assertEqual(data['phone'], self.person1.phone)
        self.assertEqual(data['address'], self.person1.address)
        self.assertEqual(data['email'], self.person1.email)
        self.assertEqual(data['has_died'], self.person1.has_died)


class PeoplePagedSerializerTestTest(SerializerTestMixin):

    def test_serializes(self):

        vm = PeopleViewModel([self.person1,], 1)
        serializer = PeoplePagedSerializer(vm)

        data = serializer.data
        self.assertIn('people', data)
        self.assertIn('num_people', data)


class CommonFriendsSerializerTestTest(SerializerTestMixin):

    def test_serializes(self):

        vm = CommonFriendsViewModel(self.person1, self.person2)
        serializer = CommonFriendsSerializer(vm)

        data = serializer.data
        self.assertIn('first_person', data)
        self.assertIn('second_person', data)
        self.assertIn('common_friends', data)


class FavouriteFoodSerializerTestTest(SerializerTestMixin):

    def test_serializes(self):

        vm = FavouriteFoodViewModel(self.person1)
        serializer = FavouriteFoodSerializer(vm)

        data = serializer.data
        self.assertIn('username', data)
        self.assertIn('age', data)
        self.assertIn('fruits', data)
        self.assertIn('vegetables', data)
