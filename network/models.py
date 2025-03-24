from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 'self' relates to class User
    # who is the user followed by
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following_users")
    # who the user follows
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers_users")

class Post(models.Model):
    content = models.TextField(max_length=250)
    likes = models.ManyToManyField(User, blank=True, related_name="users_who_liked")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID {self.id}, created by {self.creator.username}. CONTENT: {self.content}"
