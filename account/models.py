from django.db import models
from django.conf import settings
from myproject.storage_backends import PublicMediaStorage


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	description = models.TextField(blank=True)
	photo = models.ImageField(storage=PublicMediaStorage(), blank=True)

	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)