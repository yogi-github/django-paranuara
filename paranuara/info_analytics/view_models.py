from info_analytics.models import Food


class PeopleViewModel(object):

    def __init__(self, people, num_people):
        self.people = people
        self.num_people = num_people


class CommonFriendsViewModel(object):

    def __init__(self, first_person, second_person):
        self.first_person = first_person
        self.second_person = second_person

        first_person_friends = first_person.friends.filter(eye_color='brown', has_died=False).values_list('id', flat=True)
        common_friends = second_person.friends.filter(id__in=first_person_friends)
        self.common_friends = common_friends


class FavouriteFoodViewModel(object):

    def __init__(self, person):
        self.username = person.name
        self.age = person.age
        self.fruits = person.favourite_food.all().filter(type=Food.FRUITS).values_list('name', flat=True)
        self.vegetables = person.favourite_food.all().filter(type=Food.VEGETABLES).values_list('name', flat=True)
