import argparse
import json
from datetime import datetime as dt


class DataCleanser(object):
    VEGETABLES = ["beetroot", "carrot", "cucumber", "celery"]
    FRUITS = ["strawberry", "orange", "apple", "banana"]

    def __init__(self, company_file, people_file):

        self.company_file = company_file
        self.people_file = people_file
        self.food = dict()

    def get_data(self, fname):

        try:
            return json.load(open(fname))

        except Exception as ex:
            print('[get_data] Unable to load json data from file: {} err: {}'.format(fname, str(ex)))
            return list()

    def generate_model_data(self, fname, data):

        try:
            with open(fname, 'w') as file:
                json.dump(data, file)

        except Exception as ex:
            print('[generate_model_data] Unable to write json data to file: {} err: {}'.format(fname, str(ex)))

    def parse_companies(self):

        companies = []

        for value in self.get_data(self.company_file):
            try:
                companies.append(
                    {
                        "model": "info_analytics.Company",
                        "pk": value['index'] + 1,
                        "fields":
                            {
                                "name": value['company']
                            }
                    }
                )
            except KeyError as ex:
                print('[parse_companies] keyerror err: {} in value: {}'.format(str(ex), value))

        self.generate_model_data("companies.json", companies)

    def construct_food_schema(self, pk, name, type):

        # Storing the pk of each food item
        self.food[name] = pk

        return {
            "model": "info_analytics.Food",
            "pk": pk,
            "fields":
                {
                    "name": name,
                    "type": type
                }
        }

    def generate_food_data(self):

        # Get all food items
        food_lst = []

        for value in self.get_data(self.people_file):
            try:
                food_lst.extend(value['favouriteFood'])

            except KeyError as ex:
                print('[generate_food_data] keyerror err: {} in value: {}'.format(str(ex), value))

        food = []
        counter = 1

        for item in set(food_lst):
            if item in DataCleanser.VEGETABLES:
                food.append(self.construct_food_schema(counter, item, 'V'))

            elif item in DataCleanser.FRUITS:
                food.append(self.construct_food_schema(counter, item, 'F'))

            else:
                print('#########################################')
                print('Categorize food as a Vegetable or a Fruit')
                print('WARNING: Invalid choice will be skipped')
                print('#########################################')
                value = input('Is {} a Vegetable/Fruit. Enter V/F\n'.format(item))

                if value.upper() == 'V':
                    DataCleanser.VEGETABLES.append(item)
                    food.append(self.construct_food_schema(counter, item, 'V'))

                elif value.upper() == 'F':
                    DataCleanser.FRUITS.append(item)
                    food.append(self.construct_food_schema(counter, item, 'F'))

                else:
                    print('Sorry. Invalid Choice. Hence this item will be skipped')

            counter += 1

        self.generate_model_data("food.json", food)

    def parse_people(self):

        people = []

        for value in self.get_data(self.people_file):
            try:
                people.append(
                    {
                        "model": "info_analytics.Person",
                        "pk": value['index'] + 1,
                        "fields":
                            {
                                "guid": value['guid'],
                                "has_died": value['has_died'],
                                "balance": value['balance'],
                                "picture": value['picture'],
                                "age": int(value['age']),
                                "eye_color": value['eyeColor'],
                                "name": value['name'],
                                "gender": value['gender'],
                                "email": value['email'],
                                "phone": value['phone'],
                                "address": value['address'],
                                "about": value['about'],
                                "registered": str(dt.strptime(value['registered'], '%Y-%m-%dT%H:%M:%S %z')),
                                "tags": str(value['tags']),
                                "greeting": value['greeting'],
                                "company_id": value['company_id'],
                                "favourite_food": [self.food[item] for item in value['favouriteFood'] if self.food.get(item)],
                                "friends": [person['index'] + 1 for person in value['friends'] if person['index'] != value['index']]
                            }
                    }
                )

            except Exception as ex:
                print('[parse_people] err: {} in value: {}'.format(str(ex), value))

        self.generate_model_data("people.json", people)

    def start(self):

        self.parse_companies()
        self.generate_food_data()
        self.parse_people()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate Model Json')
    parser.add_argument('-c', type=str, required=True, help='Companies JSON file')
    parser.add_argument('-p', type=str, required=True, help='People JSON file')
    args = parser.parse_args()

    data_cleanser = DataCleanser(args.c.strip(), args.p.strip())
    data_cleanser.start()
