from django.urls import path
# pyrefly: ignore [missing-import]
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("ai/generate-article/", views.generate_article, name="generate_article"),
    path("post/<int:id>/", views.post_detail, name="post_detail"),
    path("post/<int:id>/publish/", views.publish_post, name="publish_post"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search, name="search"),
    path("drafts/", views.drafts, name="drafts"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)