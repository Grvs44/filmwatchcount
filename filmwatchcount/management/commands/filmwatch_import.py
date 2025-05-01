'''Import Film Watch Count data for a given user'''
# pylint:disable=no-member
from datetime import date
import json
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandParser
from django.db.transaction import atomic
from ... import models


def load_groups(user: User, data: list[dict], parent: models.FilmGroup | None):
    for item in data:
        group = models.FilmGroup.objects.create(
            User=user,
            Name=item['name'],
            FilmGroup=parent
        )
        load_groups(user, item['groups'], group)


def load_films(user: User, data: list[dict], group: models.FilmGroup | None):
    for item in data:
        film = models.Film.objects.create(
            User=user,
            Name=item['name'],
            FilmGroup=group,
            ReleaseYear=item['release_year']
        )
        load_watches(user, item['watches'], film)


def load_watches(user: User, data: list[dict], film: models.Film):
    models.FilmWatch.objects.bulk_create([models.FilmWatch(
        User=user,
        Film=film,
        DateWatched=None if item['date_watched'] is None
        else date.fromisoformat(item['date_watched']),
        Notes=item['notes']
    ) for item in data])


class Command(BaseCommand):
    help = __doc__  # type:ignore

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'username',
            help='The username of the user to import the data to'
        )
        parser.add_argument(
            'file',
            help='JSON file containing the data to import'
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Skip confirmation prompt'
        )

    @atomic
    def handle(self, *args, **options) -> None:
        username = options['username']
        file = options['file']
        user = User.objects.filter(username=username).first()
        if user is None:
            self.stderr.write(
                f'User {username} does not exist', self.style.ERROR)
            return
        if not options['no_input']:
            self.stdout.write(
                f'Import data from {file} to user {username}? (y/n)')
            if input() != 'y':
                self.stdout.write('Cancelled', self.style.SUCCESS)
                return
        with open(file) as f:
            data = json.load(f)
        load_films(user, data.get('films', []), None)
        load_groups(user, data.get('groups', []), None)
        self.stdout.write(
            f'Imported data from {file} to {username}', self.style.SUCCESS)
