from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models
# from posts.models import Post

''' Model.Manage to handle Comments for detail view'''
class CommentManager(models.Manager):
	
	def filter_by_instance(self, instance):
		content_type	= ContentType.objects.get_for_model(instance.__class__)
		obj_id       	= instance.id
		qs 				= super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
		return qs

	''' Use natural-keys to get username instead user pk '''
	def get_by_natural_key(self, user):
		return self.get(username=user.username)


class Comment(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	content_type 	= models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id 		= models.PositiveIntegerField()
	content_object 	= GenericForeignKey('content_type', 'object_id')
	content 		= models.TextField()
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects = CommentManager()

	def __unicode__(self):
		return str(self.user.username)

	#for python 3.x we use str
	def __str__(self):
		return str(self.user.username)


