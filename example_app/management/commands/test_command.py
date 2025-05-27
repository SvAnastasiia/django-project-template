# -------------------------------------------------------------------------
# To run the command: python manage.py test_command
# -------------------------------------------------------------------------

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("✅ Test successful!"))
