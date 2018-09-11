from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

""" Note: Use ModelManager to handle the model, here we gonna user it to display only those post 
at post_detail and post_list which are not set for a future date or not in the draft mode """


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

""" Note: change the upload location of the image """


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

""" Note: we use USER to associate the post to login user or super user or staff"""


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    """ Note: class model manager"""
    objects = PostManager()

    """ Note: we added a draft and publish fields as it will add up the blog functionality,
    it give an option to the staff or super user to publish the post now or save it as 
    a draft and publish at future dates """
    
    """ Note: timestamp--> It would save the time very first time when it saved in the database
    Note: updated--> Whenever we update the comment, it will save the time into the database """

    def __unicode__(self):
        return self.title

    """for python 3.x we use str"""
    def __str__(self):
        return self.title

    """ Note: get_absolute_url and reverse help to make more dynamic urls, here 'detail is the name in the url.
        e.g: url(r'^(?P<id>\d+)/$', post_detail,name='detail')'"""
	
    def get_absolute_url(self):
        # return reverse("posts:detail", kwargs={"id":self.id})
        return reverse("posts:detail", kwargs={"slug": self.slug})

	""" Note: Alternative way to order the post other than queryset at views 
	class Meta:
		ordering = ["-timestamp", "-updated"] """

	''' Comments from the site'''
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver, sender=Post)



