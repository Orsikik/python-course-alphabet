from django.db import models
from account.models import Profile
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class Article(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Article)
def notify_author(sender, instance, created, **kwargs):
    if created:
        subject = 'Article Created'
        body = 'Your article created successfully!'
        send_from = settings.DEFAULT_FROM_EMAIL
        send_to = 'orsikik@gmail.com'
        send_mail(subject, body, send_from, [send_to])


class Comments(models.Model):
    profile = models.ForeignKey(Profile, verbose_name="User", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='Article', on_delete=models.CASCADE)
    text = models.TextField("Comment")
    created = models.DateTimeField('Date:time', auto_now_add=True, null=True, blank=True)
    moderation = models.BooleanField(default=False, null=True)
    author = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=42, blank=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return "{}".format(self.profile)

    def get_absolute_url(self):
        return reverse('detail', args=(self.object.id,))


class CommentsOnComments(models.Model):
    article = models.ForeignKey(Article, verbose_name='Article', on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, verbose_name="User", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comments, verbose_name="Basecomment", on_delete=models.CASCADE)
    comment = models.TextField('Comment')

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('detail', args=(self.object.id,))