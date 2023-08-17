from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Clear expired sessions'

    def handle(self, *args, **kwargs):
        Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all sessions'))
