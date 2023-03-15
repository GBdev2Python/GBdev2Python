import os
import re
import subprocess

from pathlib import Path
from collections import defaultdict
from config.settings import BASE_DIR
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Load full project fixutures"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixtures = self.get_fixtures_files()
        self.interpreter_path = self.get_executable_path()
        self.manage_py = BASE_DIR / 'manage.py'
        self.command = 'loaddata'

    def get_app_name(self, path: str):
        re_search_pattern = re.compile(r'\w*app')
        return re_search_pattern.search(path).group()

    def get_executable_path(self):
        for dir_data in os.walk(BASE_DIR):
            current_dir, folders, files = dir_data
            for file in files:
                if file == 'python.exe' or file == 'python':
                    return str(Path(current_dir) / file)

    def get_fixtures_files(self):
        fixtures = defaultdict(list)

        for dir_data in os.walk(BASE_DIR):
            current_dir, folders, files = dir_data
            if 'fixtures' in current_dir:
                current = Path(current_dir)
                for file in files:
                    if file.endswith('.json') and 'test' not in file:
                        file_path = str(current / file)
                        fixtures[self.get_app_name(file_path)].append(file_path)

        return list(fixtures.values())

    def handle(self, *args, **options):

        for fixtures_paths in self.fixtures:
            for fixture in sorted(fixtures_paths):
                subprocess.call([self.interpreter_path, self.manage_py, self.command, fixture])