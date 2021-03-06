from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import random

class Category(models.Model):
    name = models.CharField(max_length=100)
    prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
    parent = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="child")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

class Exposition(models.Model):
    title = models.CharField(max_length=100) # title of the article or website
    link = models.CharField(max_length=100) # A URL to the location of the exposition
    cat = models.ForeignKey(Category)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Submission(models.Model):
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.CharField(max_length=400, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title

class VoteCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Vote categories"

    def __unicode__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User)
    submission = models.ForeignKey(Submission, related_name='votes')
    v_category = models.ForeignKey(VoteCategory, related_name='votes')
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s: %s: %s' % (self.user, self.submission.title, self.v_category.name)

class QuestionInstance(models.Model):
    title = models.CharField(max_length=200)
    solution = models.TextField()
    text = models.TextField()

class Choice(models.Model):
    solution = models.TextField()

class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    solution = models.TextField() #solution script location
    numChoices = models.IntegerField()

    def __unicode__(self):
        return self.title

class QuestionChoice(models.Model):
    solution = models.TextField()
    question = models.ForeignKey(Question, related_name='choices')

#consider ditching all of this for a simple name field (and make him do the randomization work)
class QuestionVariable(models.Model):
    question = models.ForeignKey(Question, related_name='variables')
    name = models.CharField(max_length=100)
    VARIABLE_TYPES = (
        ('custom', 'Custom'),
        ('int', 'Integer'),
    )
    varType = models.CharField(max_length=15, choices=VARIABLE_TYPES, default='custom')
    lowerBound = models.FloatField(default=0)
    upperBound = models.FloatField(default=0)    

    def __unicode__(self):
        return self.name

    def getValue(self):
        return random.randint(self.lowerBound, self.upperBound)