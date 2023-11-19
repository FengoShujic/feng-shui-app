install docker and login with github account

Check db
docker-compose run --rm app sh -c "python manage.py wait_for_db"

Run tests >
docker-compose run --rm app sh -c "python manage.py test"

Create app >
docker-compose run --rm app sh -c "python manage.py startapp app name"

Migrations >
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"

Runserver >
docker-compose run --rm app sh -c "python manage.py runserver"

List db >
docker volume ls

Delete volume >
docker volume rm <ime baze>

Crete admin user >
docker-compose run --rm app sh -c "python manage.py createsuperuser"