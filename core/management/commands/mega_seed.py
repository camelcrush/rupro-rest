import random
from relations.models import Relation
from faker import Faker
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from posts.models import Post
from boards.models import Board


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        user_seeder = Seed.seeder()
        user_seeder.add_entity(User, 30, {"is_staff": False})
        user_seeder.execute()

        users = User.objects.all()
        post_seeder = Seed.seeder()
        post_seeder.add_entity(
            Post,
            100,
            {
                "user": lambda x: random.choice(users),
                "title": lambda x: post_seeder.faker.sentence(),
                "description": lambda x: post_seeder.faker.sentence(),
            },
        )
        post_seeder.execute()

        fake = Faker()

        for user in users:
            Relation.objects.create(user=user)

        board_seeder = Seed.seeder()
        board_seeder.add_entity(
            Board,
            100,
            {
                "user": lambda x: random.choice(users),
                "content": lambda x: board_seeder.faker.sentence(),
            },
        )
        board_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Everything seeded"))
