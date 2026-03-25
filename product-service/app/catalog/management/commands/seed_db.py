import random
from django.core.management.base import BaseCommand
from faker import Faker
from catalog.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with mock categories and products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products",
            type=int,
            default=20,
            help="Number of products to create",
        )

    def handle(self, *args, **options):
        product_count = options["products"]

        self.stdout.write("Seeding database...")

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.unique.word().capitalize()
            )
            categories.append(category)

        # Create Products
        for _ in range(product_count):
            Product.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.text(),
                price=round(random.uniform(10, 500), 2),
                category=random.choice(categories),
                currency="USD",
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))