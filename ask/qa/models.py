from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')
    def popular(self):
        return self.order_by('-raiting')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField
    added_at = models.DateTimeField(auto_now_add=True)
    raiting = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    # def __unicode__(self):
    #     return self.title

class Answer(models.Model):
    text = models.TextField
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.OneToOneField(Question)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
