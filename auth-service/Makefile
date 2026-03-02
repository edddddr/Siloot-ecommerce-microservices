test:
	docker compose exec auth-service python manage.py test --settings=config.settings.test

coverage:
	docker compose exec auth-service coverage run --source='.' manage.py test --settings=config.settings.test
	docker compose exec auth-service coverage report