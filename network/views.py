from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    all_posts = Post.objects.all().order_by("-timestamp")
    if request.method == "POST":
        content = request.POST["content"]
        new_post = Post(content=content, creator=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/index.html", {
            "all_posts": all_posts
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def user_account(request, username):
    user = User.objects.get(username=username)
    all_posts = Post.objects.filter(creator = user.id).order_by("-timestamp")
    return render(request, "network/user_account.html", {
        "show_user": user,
        "all_posts": all_posts,
        "post_count": len(all_posts),
        "followers": user.followers.count(),
        "following": user.following.count()
    })

@login_required
def followed_posts(request):
    user = User.objects.get(username=request.user.username)
    all_posts = Post.objects.filter(creator__in=user.following.all())
    return render(request, "network/followed_posts.html", {
        "all_posts": all_posts
    })

# figure out how to distinct followers and following
# when I followed future as chester, it looks like future gave follow back instead of gaining a follower
