import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        'Load all place JSON files from a GitHub repo directory. '
        'Usage: manage.py load_places_all '
        'https://api.github.com/repos/OWNER/REPO/contents/places'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'api_url',
            help='GitHub API URL to the JSON directory, e.g. '
                 'https://api.github.com/repos/devmanorg/where-to-go-places/contents/places'
        )

    def handle(self, *args, **options):
        api_url = options['api_url']
        self.stdout.write(f'Fetching directory listing from {api_url}')
        try:
            resp = requests.get(api_url)
            resp.raise_for_status()
        except Exception as e:
            raise CommandError(f'Could not fetch directory listing: {e}')

        entries = resp.json()
        json_files = [e for e in entries
                      if e.get('type') == 'file' and e.get('name', '').endswith('.json')]

        if not json_files:
            self.stdout.write(self.style.WARNING('No JSON files found at that URL.'))
            return

        for entry in json_files:
            download_url = entry.get('download_url')
            name = entry.get('name')
            self.stdout.write(f'→ Loading {name}')
            try:
                call_command('load_place', download_url)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error loading {name}: {e}'))
        self.stdout.write(self.style.SUCCESS('Done.'))
        