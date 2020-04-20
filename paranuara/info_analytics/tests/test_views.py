from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factories import CompanyFactory, FoodFactory, PersonFactory
from ..models import Food


class GetPeoplePerCompanyViewTest(APITestCase):

    def setUp(self):

        self.client = APIClient()

        self.company1 = CompanyFactory()
        self.company2 = CompanyFactory()
        self.person1 = PersonFactory(company=self.company1)
        self.person2 = PersonFactory(company=self.company1)

        self.url = reverse('info-analytics:info-analytics.get-people', kwargs={'company_id': self.company1.id})

    def test_url(self):

        self.assertEqual('/info-analytics/get-people/company/{}'.format(self.company1.id), self.url)

    def test_get_returns_people(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEqual(data['num_people'], 2)

        person1 = data['people'][0]
        self.assertIn(person1['name'], [self.person1.name, self.person2.name])

    def test_get_with_pagination(self):

        response = self.client.get('{}?page_size=1&page_number=1'.format(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEqual(data['num_people'], 2)
        self.assertEqual(len(data['people']), 1)

    def test_get_returns_empty_list(self):

        response = self.client.get(
            reverse('info-analytics:info-analytics.get-people', kwargs={'company_id': self.company2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEqual(data['num_people'], 0)

    def test_get_returns_error_unknown_company(self):

        response = self.client.get(
            reverse('info-analytics:info-analytics.get-people', kwargs={'company_id': 12312})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCommonFriendsViewTest(APITestCase):

    def setUp(self):

        self.client = APIClient()

        self.friend1 = PersonFactory(eye_color='brown', has_died=False)
        self.friend2 = PersonFactory(eye_color='brown', has_died=True)
        self.friend3 = PersonFactory(eye_color='black')
        self.friend4 = PersonFactory(eye_color='green')
        self.friend5 = PersonFactory(eye_color='blue')

        self.person1 = PersonFactory(friends=[self.friend1, self.friend2, self.friend3, self.friend4])
        self.person2 = PersonFactory(friends=[self.friend1, self.friend2, self.friend3, self.friend5])

        self.url = reverse(
            'info-analytics:info-analytics.common-friends',
            kwargs={'first_person': self.person1.id, 'second_person': self.person2.id}
        )

    def test_url(self):

        self.assertEqual('/info-analytics/common-friends/{}/{}'.format(self.person1.id, self.person2.id), self.url)

    def test_get_returns_common_friends(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']

        person1 = data['first_person']
        self.assertEqual(person1['name'], self.person1.name)

        person2 = data['second_person']
        self.assertEqual(person2['name'], self.person2.name)

        common_friends = data['common_friends']
        self.assertEqual(len(common_friends), 1)
        self.assertEqual(common_friends[0]['name'], self.friend1.name)

    def test_get_returns_error_unknown_person(self):

        response = self.client.get(
            reverse(
                'info-analytics:info-analytics.common-friends',
                kwargs={'first_person': 10292, 'second_person': 12312}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetFavouriteFoodViewTest(APITestCase):

    def setUp(self):

        self.client = APIClient()

        self.veggie = FoodFactory(type=Food.VEGETABLES)
        self.fruit = FoodFactory(type=Food.FRUITS)
        self.person1 = PersonFactory(favourite_food=[self.veggie, self.fruit])
        self.person2 = PersonFactory()

        self.url = reverse(
            'info-analytics:info-analytics.person-food',
            kwargs={'person_id': self.person1.id}
        )

    def test_url(self):

        self.assertEqual('/info-analytics/person-food/{}'.format(self.person1.id), self.url)

    def test_get_returns_favourite_food(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEqual(data['username'], self.person1.name)
        self.assertEqual(data['age'], self.person1.age)
        self.assertIn(self.veggie.name, data['vegetables'])
        self.assertIn(self.fruit.name, data['fruits'])

    def test_get_favourite_food_returns_empty(self):

        response = self.client.get(
            reverse(
                'info-analytics:info-analytics.person-food',
                kwargs={'person_id': self.person2.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['data']
        self.assertEqual(data['username'], self.person2.name)
        self.assertEqual(data['age'], self.person2.age)
        self.assertEqual(len(data['vegetables']), 0)
        self.assertEqual(len(data['fruits']), 0)

    def test_get_returns_error_unknown_person(self):

        response = self.client.get(
            reverse(
                'info-analytics:info-analytics.person-food',
                kwargs={'person_id': 10202}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)