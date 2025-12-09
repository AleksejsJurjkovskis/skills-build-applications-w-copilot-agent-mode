from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='dc', description='DC superheroes')

        # Create users
        users = [
            User(email='ironman@marvel.com', name='Iron Man', team='marvel', is_superhero=True),
            User(email='spiderman@marvel.com', name='Spider-Man', team='marvel', is_superhero=True),
            User(email='batman@dc.com', name='Batman', team='dc', is_superhero=True),
            User(email='wonderwoman@dc.com', name='Wonder Woman', team='dc', is_superhero=True),
        ]
        User.objects.bulk_create(users)

        # Create activities
        for user in User.objects.all():
            Activity.objects.create(user=user, type='run', duration=30)
            Activity.objects.create(user=user, type='swim', duration=45)

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        # Create workouts
        Workout.objects.create(name='Pushups', description='Do pushups', suggested_for='marvel')
        Workout.objects.create(name='Squats', description='Do squats', suggested_for='dc')

        # Ensure unique index on email field
        with connection.cursor() as cursor:
            cursor.execute('''
                db = connection.get_database()
                db.users.createIndex({ "email": 1 }, { "unique": true })
            ''')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
