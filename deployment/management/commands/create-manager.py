import random
import string

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the manager superuser account if does not exists."

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Username to use for login (default: tbhaxor)", default="astrodata")
        parser.add_argument("--password", help="Password for the admin account to use. If not passed, it will generate and print on stdout")
        parser.add_argument("--silent", default=False, action="store_true", help="Should not throw command error when set")

    def handle(self, *args, **options):
        password = options.get("password")
        username = options.get("username")

        user = User.objects.filter(username=username).first()
        if user is not None:
            msg = f"Username {username} already exists."
            if options["silent"]:
                self.stdout.write(self.style.WARNING(f"{msg} Skipping...."))
                return
            raise CommandError(msg)

        if password is None:
            password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
            self.stdout.write(self.style.SUCCESS(f"The password for {username} is {password}."))
            self.stdout.write(self.style.SUCCESS("We recommend you to change it after first login."))

        User.objects.create_superuser(username=username, password=password)
