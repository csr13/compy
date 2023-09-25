from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):

    help = "Creates the default user"

    user = {
        "email" : "admin@compliance.com",
        "username" : "admin",
        "password" : "Admin!#%135",
    }

    def add_arguments(self, parser):
        return None

    def handle(self, *args, **options):
        if User.objects.filter(
                email=self.user["email"],
                is_superuser=True,
                is_active=True,
                is_staff=True
            ).exists():
            self.stdout.write(self.style.SUCCESS("Super exists user Details:"))
            for k, v in self.user.items():
                self.stdout.write(self.style.ERROR("{} => {}".format(k, v)))
                exit(0)

        User.objects.create_superuser(**self.user)
        self.stdout.write(self.style.SUCCESS("Super user Details:"))
        for k, v in self.user.items():
            self.stdout.write(self.style.ERROR("{} => {}".format(k, v)))
        exit(0)
