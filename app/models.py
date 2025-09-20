import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from app.managers import UserProfileManager

# Create your models here.
class UserProfile(AbstractUser):
    @property
    def article_count(self):
        return self.articles.count() # type:ignore
    
    @property
    def written_word(self):
        return self.articles.aggregate(models.Sum('word_count'))['word_count__sum'] or 0 # type:ignore


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, default='')
    word_count = models.IntegerField(blank=True, default='') #type:ignore
    twitter_post = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('published', 'Published'),
    ], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Authentication
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        text = re.sub("r<[A]*>", "", self.content).replace("&nbsp;", " ")
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
