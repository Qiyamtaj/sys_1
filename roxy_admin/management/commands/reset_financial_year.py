from datetime import date
from django.core.management.base import BaseCommand
from roxy_admin.models import Volunteer, Surfer

class Command(BaseCommand):
    help = 'Reset hours and attendance for the new financial year'

    def handle(self, *args, **kwargs):
        current_year = date.today().year
        # Reset hours and attendance for Volunteer and Surfer models
        Volunteer.objects.filter(financial_year=current_year).update(hours=0.0, attendance=0)
        Surfer.objects.filter(financial_year=current_year).update(hours=0.0, attendance=0)
        self.stdout.write(self.style.SUCCESS('Successfully reset hours and attendance for the new financial year'))
