import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def save_edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_to_edit = Post.objects.get(id=data.get("post_id"))
        if post_to_edit.creator == request.user:
            post_to_edit.content = data.get("edit")
            post_to_edit.save()
            return JsonResponse({}, status=201)
    else:
        return HttpResponseRedirect(reverse('index'))
    
@csrf_exempt
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)

        follow_request = User.objects.get(username = request.user.username)
        follow_who = User.objects.get(username = data.get("follow_who"))

        if follow_request.following.filter(username=follow_who.username).exists():
            follow_request.following.remove(follow_who)
            follow_who.followers.remove(follow_request)
            print(f"{follow_request} just unfollowed {follow_who}")
        else:
            follow_request.following.add(follow_who)
            follow_who.followers.add(follow_request)
            print(f"{follow_request} just followed {follow_who}")

        follow_request.save()
        follow_who.save()

        return JsonResponse({}, status=201)

    else:
        return HttpResponseRedirect(reverse('index')) 