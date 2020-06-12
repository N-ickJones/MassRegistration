from django.core.management.base import BaseCommand, CommandError

import time
from threading import Timer, Thread


class Command(BaseCommand):
    help = 'Creates Task Scheduler for Booking Table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = None
        self.interval = 5
        self.is_running = False
        self.thread = None

    def add_arguments(self, parser):
        # Accepts only one argument
        parser.add_argument('action', nargs=1, type=str)

    def handle(self, *args, **options):
        action = options['action'][0]

        if action == 'run':
            print('temporary: Running Booking update.')