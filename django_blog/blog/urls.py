from django.urls import path
# pyrefly: ignore [missing-import]
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("post/<int:id>/",views.post_detail,name="post_detail"),
]