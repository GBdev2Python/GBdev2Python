import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Load full project fixutures"
    )

    def handle(self, *args, **options):
        print(subprocess.call(
            ['./venv/Scripts/python.exe', './manage.py', 'loaddata', r'.\applicantapp\fixtures\001_applicants.json']
        ))
