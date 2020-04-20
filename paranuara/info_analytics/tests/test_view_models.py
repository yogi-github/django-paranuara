from django.test import TestCase

from info_analytics.models import Food
from info_analytics.tests.factories import PersonFactory, FoodFactory, CompanyFactory
from info_analytics.view_models import PeopleViewModel, CommonFriendsViewModel, FavouriteFoodViewModel


class ViewModelTestMixin(TestCase):

    def setUp(self):

        self.company = CompanyFactory()

        self.friend1 = PersonFactory(eye_color='brown', has_died=False)
        self.friend2 = PersonFactory(eye_color='brown', has_died=True)
        self.friend3 = PersonFactory(eye_color='black')
        self.friend4 = PersonFactory(eye_color='green')
        self.friend5 = PersonFactory(eye_color='blue')

        self.veggie = FoodFactory(type=Food.VEGETABLES)
        self.fruit = FoodFactory(type=Food.FRUITS)

        self.person1 = PersonFactory(
            company=self.company,
            friends=[self.friend1, self.friend2, self.friend3, self.friend4],
            favourite_food=[self.veggie, self.fruit]
        )
        self.person2 = PersonFactory(
            company=self.company,
            friends=[self.friend1, self.friend2, self.friend3, self.friend5]
        )


class PeopleViewModelTest(ViewModelTestMixin):

    def test_init(self):

        vm = PeopleViewModel([self.person1, self.person2], 2)
        self.assertEqual(vm.num_people, 2)
        self.assertEqual(vm.people, [self.person1, self.person2])


class CommonFriendsViewModelTest(ViewModelTestMixin):

    def test_init(self):

        vm = CommonFriendsViewModel(self.person1, self.person2)
        self.assertEqual(vm.first_person, self.person1)
        self.assertEqual(vm.second_person, self.person2)
        self.assertEqual(list(vm.common_friends), [self.friend1,])


class FavouriteFoodViewModelTest(ViewModelTestMixin):

    def test_init(self):

        vm = FavouriteFoodViewModel(self.person1)
        self.assertEqual(vm.username, self.person1.name)
        self.assertEqual(vm.age, self.person1.age)
        self.assertEqual(list(vm.fruits), [self.fruit.name,])
        self.assertEqual(list(vm.vegetables), [self.veggie.name,])