from django.core.management.base import BaseCommand
from library.dbfactories import AuthorFactory, BookFactory, PublisherFactory, UserFactory, StudentFactory, LibrarianFactory

class Command(BaseCommand):
    help = 'Seeds the database.'

    def add_arguments(self, parser):
        parser.add_argument('--users',
            default=400,
            type=int,
            help='The number of fake users to create.')

    def handle(self, *args, **options):
        for _ in range(options['users']):
            PublisherFactory.create()
            AuthorFactory.create()
            BookFactory.create()
            UserFactory.create()
            StudentFactory.create()
            LibrarianFactory.create()