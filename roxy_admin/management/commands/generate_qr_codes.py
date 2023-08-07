from django.core.management.base import BaseCommand
from roxy_admin.models import Surfer, Volunteer

class Command(BaseCommand):
    help = 'Generate QR codes for all surfers and volunteers'

    def handle(self, *args, **options):
        for surfer in Surfer.objects.all():
            surfer.save()

        for volunteer in Volunteer.objects.all():
            volunteer.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated QR codes for all surfers and volunteers'))