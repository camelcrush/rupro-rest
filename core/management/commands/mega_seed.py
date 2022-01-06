import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from posts.models import Post
from boards.models import Board
from games.models import Game


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        game_seeder = Seed.seeder()
        game_seeder.add_entity(Game, 10)
        game_seeder.execute()

        user_seeder = Seed.seeder()
        user_seeder.add_entity(User, 30, {"is_staff": False})
        user_seeder.execute()

        users = User.objects.all()
        games = Game.objects.all()
        post_seeder = Seed.seeder()
        post_seeder.add_entity(
            Post,
            100,
            {
                "user": lambda x: random.choice(users),
                "title": lambda x: post_seeder.faker.sentence(),
                "description": lambda x: post_seeder.faker.sentence(),
                "game": lambda x: random.choice(games),
            },
        )
        post_seeder.execute()

        board_seeder = Seed.seeder()
        board_seeder.add_entity(
            Board,
            100,
            {
                "user": lambda x: random.choice(users),
                "content": lambda x: board_seeder.faker.sentence(),
                "game": lambda x: random.choice(games),
            },
        )
        board_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Everything seeded"))
