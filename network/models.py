from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "id": self.pk,
            "username": self.username
        }

class Tweet(models.Model):
    content = models.CharField(max_length=300)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allPosts")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField("User", blank=True, related_name="likes_given")

    def __str__(self):
        return f"User:{self.id_user} content:{self.content} time:{self.created_at} "

    def serialize(self):
        return {
            "id": self.pk,
            "content": self.content,
            "id_user": self.id_user,
            "created_at": self.created_at,
            "update_at": self.update_at,
            "likes": self.likes
        }

class Relationship(models.Model):
    id_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfollowing")
    id_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Follower:{self.id_follower} followed:{self.id_followed}"


class Comments(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comment")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id_user": self.id_user,
            "id_tweet": self.id_tweet,
            "comment": self.comment,
            "time": self.time.strftime("%b %d %Y, %I:%M %p")
        }

class images(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def serialize(self):
        return {
            "id_user": self.id_user,
            "profile_image": str(self.profile_image.path)
        }

    def __str__(self):
        return f"Id:{self.id_user} profile_image:{self.profile_image}"