#!/bin/bash

sets_up() {
  echo "..."
  echo "Start Setup"
  echo "..."
  echo "Install Libraries"
  echo "...\n"
  pip install -r requirements.txt
}

apply_migration() {
  echo "..."
  echo "Apply DB Migration"
  echo "...\n"
  cd ./paranuara
  python manage.py migrate info_analytics
  cd ..
}

load_data() {
  echo "..."
  echo "Format data"
  cd ./paranuara/info_analytics/fixtures/
  rm companies.json people.json food.json
  python format_data.py -c ./resources/companies.json -p ./resources/people.json
  cd ../..
  echo "Format data completed"
  echo "Load data"
  echo "...\n"
  python manage.py loaddata companies
  python manage.py loaddata food
  python manage.py loaddata people
  cd ..
}

start_server() {
  echo "..."
  echo "Running Django development server"
  echo "...\n"
  cd ./paranuara
  python manage.py runserver
}

clear_data() {
  echo "..."
  echo "Clear data"
  echo "...\n"
  cd ./paranuara
  python manage.py migrate info_analytics zero
  cd ..
}

usage() {
  echo "Usage: $0
  [-a start <Setup everything>]
  [-l start <Load new data and start the server>]
  [-c start <clear data and migrations>]"
  1>&2;
  exit 1;
}

while getopts ":a:l:c:" o;
do
    case "${o}" in
        a)
            sets_up
            apply_migration
            load_data
            start_server
            ;;
        l)
            clear_data
            apply_migration
            load_data
            start_server
            ;;
        c)
            clear_data
            exit 0
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${a}" ] || [ -z "${l}" ] ||  [ -z "${c}" ]; then
    usage
fi