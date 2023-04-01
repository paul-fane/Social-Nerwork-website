import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import User, Tweet, Relationship, Comments, images
from .forms import TweetForm, imagesForm


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = TweetForm(request.POST)
        if form.is_valid():
            Tweet.objects.create(content=request.POST['content'], id_user=request.user)
            return HttpResponseRedirect(reverse("index"))

    # Querri for all posts
    list_tweet = Tweet.objects.all().order_by('-created_at')

    # Create 10 object per pagin
    paginator = Paginator(list_tweet, 10)

    # Get the number page from the client
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    # Get the userneme 
    if (request.user.username):
        getuser = User.objects.get(username=request.user.username)
        
        try:
            profileImage = images.objects.get(id_user=getuser.id)
        except images.DoesNotExist:
            profileImage = False
    else:
        profileImage = ""

    
    return render(request, "network/index.html", {
        "form": TweetForm,
        "page_obj": page_obj,
        "image": profileImage
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username,  email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profilePage(request, profileName):

    # Get the userneme 
    getuser = User.objects.get(username=profileName)
    # Count the followers
    followers = getuser.followers.all().count()
    # Return the posts in reverse order
    posts = Tweet.objects.filter(id_user=getuser.id).order_by('-created_at')
    # Return the number posts 
    numberPosts = Tweet.objects.filter(id_user=getuser.id).count()
    # Count the following
    following = Relationship.objects.filter(id_follower=getuser.id).count()
    # Return the login user
    loginUser = request.user
    # Is the login user in the people that the profile user follow
    relation = Relationship.objects.filter(id_follower=loginUser.id, id_followed=getuser.id)

    if(len(relation)== 0):
        follow = False
    else:
        follow = True 

    followersprofile = getuser.followers.all()
    followingprofile = Relationship.objects.filter(id_follower=getuser.id)

    # Create 10 object per pagin
    paginator = Paginator(posts, 10)

    # Get the number page from the client
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profileImage = images.objects.filter(id_user=getuser.id).last

    # Get the userneme 
    if (request.user.username):
        currentUser = User.objects.get(username=request.user.username)
        try:
            currentUserProfileImage = images.objects.get(id_user=currentUser.id)
        except images.DoesNotExist:
            currentUserProfileImage = False
    else:
        currentUserProfileImage = ""

    return render(request, "network/profilePage.html", {
        "profiluser": getuser,
        "numFollowers": followers,
        "page_obj": page_obj,
        "numFollowing": following,
        "loginUser": loginUser,
        "follow" : follow,
        "form": imagesForm,
        "image": profileImage,
        "numberPosts": numberPosts,
        "currentUserProfileImage": currentUserProfileImage,

        "profile": followersprofile,
        "followingprofile": followingprofile
    })


@login_required
def addProfileImage(request, profileName):
    if request.user.username == profileName:
        if request.method == "POST":
            form = imagesForm(request.POST, request.FILES)
            if form.is_valid():
                #
                getuser = User.objects.get(username=profileName)
                try:
                    profileImage = images.objects.get(id_user=getuser)
                    if profileImage:
                        profileImage.delete()
                except:
                    pass
                #
                image = form.save(commit=False)
                image.id_user = request.user
                image.save()
                return HttpResponseRedirect(reverse("profilePage", args=(request.user, )))
    
    return HttpResponseRedirect(reverse("profilePage", args=(profileName, )))

@login_required
def followingPosts(request):

    # All current user relationship
    followingUsers = request.user.myfollowing.all()

    # All person that current user follow
    followingPersons = []
    for relationship in followingUsers:
        followingPersons.append(relationship.id_followed)

    # Get all posts from users that current user follows
    #posts = [users.id_followed.allPosts.all() for users in followingUsers]
    # Flatten 2d array to 1d array
    #posts = list(chain(*posts))

    allPosts = Tweet.objects.filter(id_user__in=followingPersons).order_by('-created_at')

    # Create 10 object per pagin
    paginator = Paginator(allPosts, 10)

    # Get the number page from the client
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the userneme 
    if (request.user.username):
        getuser = User.objects.get(username=request.user.username)
        
        try:
            profileImage = images.objects.get(id_user=getuser.id)
        except images.DoesNotExist:
            profileImage = False
    else:
        profileImage = ""
    
    return render(request, "network/following.html", {
        "form": TweetForm,
        "page_obj": page_obj,
        "image" : profileImage
    })


@login_required
def followButton(request, profileName):
    username = User.objects.filter(username=profileName)[0]
    relation = Relationship.objects.filter(id_follower=request.user, id_followed=username.id)

    # Check if there is relationship
    if(len(relation)== 0):
        relation = False
    else:
        relation = True 

    return JsonResponse({"relation": relation}, status=201)


@login_required
def addfollow(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("profileUser") is not None:
            username = User.objects.filter(username=data['profileUser'])[0]
            Relationship.objects.create(id_follower=request.user, id_followed=username)
            numFollowers=username.followers.all().count()
            return JsonResponse({"numFollowers": numFollowers}, status=201)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def removefollow(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("profileUser") is not None:
            username = User.objects.filter(username=data['profileUser'])[0]
            Relationship.objects.get(id_follower=request.user, id_followed=username.id).delete()
            numFollowers=username.followers.all().count()
            return JsonResponse({"numFollowers": numFollowers}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@login_required
def editcontent(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        # Get contents of post
        newContent = data.get("newContent", "")
        postid = data.get("postid", "")

        try:
            tweet = Tweet.objects.get(id=postid)
        except Tweet.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        if request.user != tweet.id_user:
            return JsonResponse({"error": "Can only edit your own posts"})
        tweet.content = newContent
        tweet.save()

        return JsonResponse({"message": "Post edited successfully"}, status=201)

    return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        # Get content
        postid = data.get("postid", "")

        try:
            tweet = Tweet.objects.get(pk=postid)
        except Tweet.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        # A flag for the action addlike or remove like
        addlike = True

        # If the user is in the list of like then add like else remove like
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
            addlike = False
        else:
            tweet.likes.add(request.user)
        tweet.save()

        # Count the number of likes
        numlike = tweet.likes.all().count()
        return JsonResponse({"message": "Like successfully", "addlike": addlike, "numlike": numlike}, status=201)

    return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def comments(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        # Get content
        #newComment =data.get("newComment","")
        #postid = data.get("postid", "")

        newComment =data['newComment']
        postid = data['postid']
        
        try:
            tweet = Tweet.objects.get(pk=postid)
        except Tweet.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        comment = Comments.objects.create(id_user=request.user, id_tweet=tweet, comment=newComment)
        comment.save()

        numberComments = tweet.comment.all().count()
        currentUser = User.objects.get(username=request.user.username)

        # Get the userneme 
        if (request.user.username):
            getuser = User.objects.get(username=request.user.username)
            
            try:
                profileImage = images.objects.get(id_user=getuser.id)
                image = str(profileImage.profile_image)
            except images.DoesNotExist:
                image = "noImage"

        return JsonResponse({
            "message": "Successfully",
            "currentUser": currentUser.serialize(), 
            "numberComments":numberComments,
            "image": image
            }, status=201)

    return JsonResponse({"error": "POST request required."}, status=400)


def search(request, profileName):
    if request.method == "GET":
        # Get content
        #q = request.GET.get('q', '')
        #print(q)
        try:
            allUser = User.objects.filter(username__icontains=profileName)
        except Tweet.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        return JsonResponse([person.serialize() for person in allUser], safe=False)


    return JsonResponse({"error": "GET request required."}, status=400)


def searchLikes(request, postNumber):
    tweet = Tweet.objects.get(pk=postNumber)
    print(tweet.likes.all())
    
    return JsonResponse({"person":[person.serialize() for person in tweet.likes.all()]}, safe=False)


def searchFollowers(request, profileName):
    # Get the userneme 
    getuser = User.objects.get(username=profileName)

    # Relationship list
    relationships = getuser.followers.all()
    # Return the list of user that follow the curent profile user
    return JsonResponse([relation.id_follower.serialize() for relation in relationships], safe=False)

def searchFollowing(request, profileName):
    # Get the userneme 
    getuser = User.objects.get(username=profileName)

    # Relationship list
    relationships = getuser.myfollowing.all()
    # Return the list of user that the curent profile user are following
    return JsonResponse([relation.id_followed.serialize() for relation in relationships], safe=False)


def searchImage(request, profileName):
    # Get the userneme 
    getuser = User.objects.get(username=profileName)
    #profileImage = images.objects.filter(id_user=getuser).last
    try:
        profileImage = images.objects.get(id_user=getuser)
        image = str(profileImage.profile_image)

        return JsonResponse({"image": image }, status=201)
    except images.DoesNotExist:
        return JsonResponse({"image": "noImage" }, status=201)


def searchCommentImage(request, profileName):
    # Get the userneme 
    getuser = User.objects.get(username=profileName)
    #profileImage = images.objects.filter(id_user=getuser).last
    try:
        profileImage = images.objects.get(id_user=getuser)
        image = str(profileImage.profile_image)

        return JsonResponse({"image": image }, status=201)
    except images.DoesNotExist:
        return JsonResponse({"image": "noImage" }, status=201)
    