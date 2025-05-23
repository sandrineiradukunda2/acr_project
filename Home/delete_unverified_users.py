from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import User

class Command(BaseCommand):
    help = "Delete users whose verification expired"

    def handle(self, *args, **kwargs):
        User.objects.filter(is_verified=False, token_expiry__lt=timezone.now()).delete()
