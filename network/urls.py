
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile-<str:profileName>", views.profilePage, name="profilePage"),
    path("follow-button/<str:profileName>", views.followButton, name="follow-button"),
    path("following-posts", views.followingPosts, name="following-posts"),
    path("addfollow", views.addfollow, name="addfollow"),
    path("removefollow", views.removefollow, name="removefollow"),
    path("editcontent", views.editcontent, name="editcontent"),
    path("like", views.like, name="like"),
    path("comments", views.comments, name="comments"),
    path("search/<str:profileName>", views.search, name="search"),
    path("likesList/<int:postNumber>", views.searchLikes, name="searchLikes"),
    path("followersList/<str:profileName>", views.searchFollowers, name="searchFollowers"),
    path("followingList/<str:profileName>", views.searchFollowing, name="searchFollowing"),
    path("addProfileImage-<str:profileName>", views.addProfileImage, name="addProfileImage"),
    path("image/<str:profileName>", views.searchImage, name="searchImage"),
    path("comment-image/<str:profileName>", views.searchCommentImage, name="searchImage")
]
