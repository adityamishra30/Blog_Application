from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


STATUS_CHOICES = [
    ("draft", "Draft"),
    ("published", "Published"),
]


class Blog(models.Model):

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    cover_image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    is_ai_generated = models.BooleanField(default=False)
    generation_topic = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "story"
            slug = base_slug
            count = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/default.png"
    )

    bio = models.TextField(
        max_length=250,
        blank=True
    )

    followers = models.ManyToManyField(
        User,
        related_name="following",
        blank=True
    )

    def __str__(self):
        return self.user.username