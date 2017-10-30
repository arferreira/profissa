clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.py.swp" -exec rm -rf {} \;

run:clean
	python manage.py runserver

shell:clean
	python manage.py shell

migrate:clean
	python manage.py migrate

migrations:clean
	python manage.py makemigrations

superuser:clean
	python manage.py createsuperuser

tests:clean
	python manage.py test
