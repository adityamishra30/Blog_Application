from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Blog, Profile


class BlogAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Password123!"
        )

    def test_profile_creation_signal(self):
        """Test that profile is automatically created when a user is created."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_user_registration(self):
        """Test registration endpoint with valid data."""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_blog_slug_generation(self):
        """Test automatic slug generation on blog save."""
        post = Blog.objects.create(
            title="My First Test Post",
            content="Hello world",
            author=self.user,
            status="published"
        )
        self.assertEqual(post.slug, "my-first-test-post")

    def test_home_view(self):
        """Test home feed view displays published posts."""
        Blog.objects.create(
            title="Published Post",
            content="Published content",
            author=self.user,
            status="published"
        )
        self.client.login(username="testuser", password="Password123!")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")
