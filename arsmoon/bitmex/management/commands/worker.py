from django.core.management import BaseCommand
import time
from arsmoon.bitmex.websockets.workers import BitmexWorker


class Command(BaseCommand):

    def handle(self, *args, **options):
        worker = BitmexWorker()
        try:
            worker.run()
        except KeyboardInterrupt:
            pass
        finally:
            print('Shutdown worker...')
            worker.shutdown()
