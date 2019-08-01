from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset()\
								.filter(active=True)


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
	body = models.TextField()
	active = models.BooleanField(default=True)
	user_like = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_posts', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		ordering = ('-created', )

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("post_detail", args=[self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name