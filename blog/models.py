from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from myproject.storage_backends import PublicMediaStorage


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset()\
								.filter(active=True)


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	image = models.ImageField(storage=PublicMediaStorage(), blank=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
	body = models.TextField()
	active = models.BooleanField(default=True)
	user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
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

	def get_total_comment(self):
		 return Comment.objects.filter(Q(post=self) | Q(reply__post=self)).count()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)


class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)


class Comment(models.Model):
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
	user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)
	body = models.TextField()
	reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "'{}' bình luận bài viết".format(self.user.username)
