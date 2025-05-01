'''Export Film Watch Count data for a given user'''
# pylint:disable=no-member
import json
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandParser
from ... import models


def find_groups(user: User, parent: models.FilmGroup | None):
    groups = models.FilmGroup.objects.filter(User=user, FilmGroup=parent).all()
    return [{
        'name': group.Name,
        'groups': find_groups(user, group),
        'films': find_films(user, group),
    } for group in groups]


def find_films(user: User, group: models.FilmGroup | None):
    films = models.Film.objects.filter(User=user, FilmGroup=group).all()
    return [{
        'name': film.Name,
        'release_year': film.ReleaseYear,
        'watches': find_watched(user, film),
    } for film in films]


def find_watched(user: User, film: models.Film):
    watches = models.FilmWatch.objects.filter(User=user, Film=film).all()
    return [{
        'date_watched': None if watch.DateWatched is None else watch.DateWatched.isoformat(),
        'notes': watch.Notes,
    } for watch in watches]


class Command(BaseCommand):
    help = __doc__  # type:ignore

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'username',
            help='The username of the user to export the data of'
        )
        parser.add_argument(
            '-i', '--indent',
            default=None,
            type=int,
            help='Indent for pretty-printing JSON output (default: no pretty-print)'
        )

    def handle(self, *args, **options) -> None:
        username = options['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            self.stderr.write(
                f'User {username} does not exist', self.style.ERROR)
            return
        result = {'films': find_films(
            user, None), 'groups': find_groups(user, None)}
        self.stdout.write(json.dumps(result, indent=options['indent']))
