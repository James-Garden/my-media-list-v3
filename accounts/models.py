from django.contrib.auth.models import AbstractUser

from media.models import Media


class User(AbstractUser):
    def __str__(self):
        return f"<User: [{self.username}]>"
