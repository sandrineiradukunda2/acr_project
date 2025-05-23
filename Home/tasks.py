import csv
from datetime import timezone
from celery import shared_task
from django.conf import settings
from django.utils.timezone import now
from .models import User
import os

@shared_task
def backup_user_data_csv():
    """Backup user data to a CSV file."""
    try:
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)  # Ensure directory exists

        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(backup_dir, f'user_backup_{timestamp}.csv')

        with open(backup_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['First Name', 'Last Name', 'Username', 'Email', 'Gender', 'DOB'])

            for user in User.objects.all():
                writer.writerow([user.first_name, user.last_name, user.username, user.email, user.gender, user.dob])

        return f"Backup successful: {backup_file}"

    except Exception as e:
        return f"Backup failed: {str(e)}"
    from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def delete_unverified_users():
    unverified_users = User.objects.filter(is_verified=False, token_expiry__lt=timezone.now())
    unverified_users.delete()

