# Paranuara
Language: Python

Framework: Django

DB: sqlite3 [Django Inbuilt]

## Environment
Assuming following environment is in the target system.

- Python 3.7
- Mac OS/Linux

### Setting the virtual environment
From the project root directory, use 'python3' if various versions are used, else 'python'
- python3 -m pip install virtualenv
- python3 -m virtualenv ENV
- source ENV/bin/activate

## Setup Script
Input Data such as  companies.json and people.json are placed in the following location:
**paranuara\info_analytics\fixtures\resources**

Setup Script does the following:
- Installs dependent libraries
- Applies DB Migration
- Formats the resource files and Loads JSON data into the Database
- Starts the Django web server and application starts running on http://127.0.0.1:8000

### Execute script
From project root directory
> sh setup.sh -a start

## Endpoints
Once Django server started, following endpoints can be tested using Postman or other ways:

- Given a company, return all their employees. Pagination is optional.

> **http://127.0.0.1:8000/info-analytics/get-people/company/<company_id>?page_size=<>&page_number=<>**

```json
GET
http://127.0.0.1:8000/info-analytics/get-people/company/50?page_size=5&page_number=1

Response
{
    "data": {
        "people": [
            {
                "id": 903,
                "name": "Carey Olsen",
                "age": 22,
                "email": "careyolsen@earthmark.com",
                "address": "473 Lott Street, Loretto, Montana, 656",
                "phone": "+1 (832) 461-2297",
                "has_died": true
            },
            {
                "id": 591,
                "name": "Charles Oneal",
                "age": 32,
                "email": "charlesoneal@earthmark.com",
                "address": "212 Ridgewood Place, Gratton, Indiana, 2565",
                "phone": "+1 (851) 529-2314",
                "has_died": false
            }
        ],
        "num_people": 16
    },
    "status_message": "ok",
    "message": null
}
```

- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.

> **http://127.0.0.1:8000/info-analytics/common-friends/<first_person>/<second_person>**

```json
GET
http://127.0.0.1:8000/info-analytics/common-friends/10/50

Response
{
    "data": {
        "first_person": {
            "id": 10,
            "name": "Henderson Petty",
            "age": 26,
            "email": "hendersonpetty@earthmark.com",
            "address": "129 Beach Place, Gorham, District Of Columbia, 2637",
            "phone": "+1 (802) 558-2744",
            "has_died": true
        },
        "second_person": {
            "id": 50,
            "name": "Cross Roman",
            "age": 34,
            "email": "crossroman@earthmark.com",
            "address": "377 Will Place, Skyland, Pennsylvania, 3968",
            "phone": "+1 (901) 529-3229",
            "has_died": false
        },
        "common_friends": [
            {
                "id": 2,
                "name": "Decker Mckenzie",
                "age": 60,
                "email": "deckermckenzie@earthmark.com",
                "address": "492 Stockton Street, Lawrence, Guam, 4854",
                "phone": "+1 (893) 587-3311",
                "has_died": false
            }
        ]
    },
    "status_message": "ok",
    "message": null
}
```

- Given 1 people, provide a list of fruits and vegetables they like.

> **http://127.0.0.1:8000/info-analytics/person-food/<person_id>**

```json
GET
http://127.0.0.1:8000/info-analytics/person-food/10

Response
{
    "data": {
        "username": "Henderson Petty",
        "age": 26,
        "fruits": [
            "apple",
            "banana"
        ],
        "vegetables": [
            "celery",
            "cucumber"
        ]
    },
    "status_message": "ok",
    "message": null
}
```

## Testing with different input data

Input Data such as companies.json and people.json are placed in the following location:
**paranuara\info_analytics\fixtures\resources**

Kindly follow the file naming convention - companies.json and people.json. Else application will throw error.

### Execute script to load data and start the server
From project root directory
> sh setup.sh -l start

## Additional Info
### Starting Django Server Manually
> cd paranuara

> python manage.py runserver

### Execute unit tests
> cd paranuara

> python manage.py test 

App specific test cases
> python manage.py test info_analytics
