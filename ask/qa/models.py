from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class QuestionManager(models.Manager):
    def new(self):
        #return self.order_by('-id')
        return self.order_by('-added_at')
    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField(default='')
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='question_like_user', blank=True)
    def __unicode__(self):
        return self.title
    def get_url(self):
        return "/question/{}/".format(self.id)
        #return reverse('question-details', kwargs={'id': str(self.id)})

class Answer(models.Model):
    text = models.TextField(default='')
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __unicode__(self):
        return len(self.text)>50 and self.text[:50]+"..." or self.text
