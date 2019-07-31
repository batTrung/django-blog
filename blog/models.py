from django.db import models
from django.conf import settings


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)
	image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
	body = models.TextField()
	user_like = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_posts', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created', )

	def __str__(self):
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name