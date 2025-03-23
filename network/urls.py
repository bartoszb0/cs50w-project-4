
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.followed_posts, name="followed_posts"),
    path("saveedit", views.save_edit, name="saveedit"),
    path("handlefollow", views.follow, name="handlefollow"),
    path("<str:username>", views.user_account, name="user_account"),
]
