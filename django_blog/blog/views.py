# pyrefly: ignore [missing-import]
from .models import Blog,Profile
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from .forms import BlogForm,ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# pyrefly: ignore [missing-import]
from .services.ai import generate_article

def logout_view(request):
    logout(request)
    return redirect("login")




def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "blog/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "blog/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "blog/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already registered.")
            return render(request, "blog/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)

        return redirect("home")

    return render(request, "blog/register.html")

@login_required
def home(request):
    posts=Blog.objects.filter(status="published").order_by("-created_at")
    
    context={
        "posts":posts
    }

    return render(request,"blog/home.html",context)

@login_required
def create_post(request):

    if request.method == "POST":

        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():

            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            return redirect("home")

    else:
        form = BlogForm()

    context = {
        "form": form
    }

    return render(request, "blog/create_post.html", context)

@require_POST
@login_required
def generate_blog(request):

    title = request.POST.get("title", "").strip()

    if not title:
        return JsonResponse(
            {"error": "Please enter a title."},
            status=400,
        )

    try:
        article = generate_article(title)

        return JsonResponse({
            "content": article
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500,
        )

def post_detail(request, id):
    post = get_object_or_404(Blog, id=id)

    if post.status != "published" and post.author != request.user:
        return HttpResponse("Unauthorized", status=403)

    context = {
        "post": post
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )


@login_required
def profile(request):

    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    published_posts = Blog.objects.filter(
        author=request.user,
        status="published"
    ).order_by("-created_at")

    draft_posts = Blog.objects.filter(
        author=request.user,
        status="draft"
    ).order_by("-created_at")

    context = {
        "profile": profile,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
    }

    return render(
        request,
        "blog/profile.html",
        context
    )
    
    
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form=ProfileForm(instance=profile)
    
    context={
        "form":form
    }

    return render(request,"blog/edit_profile.html",context)

@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = (
            Blog.objects.filter(status="published", title__icontains=query) |
            Blog.objects.filter(status="published", content__icontains=query)
        ).distinct().order_by("-created_at")
    return render(request, "blog/search.html", {"results": results})


@login_required
def drafts(request):
    draft_posts = Blog.objects.filter(
        author=request.user,
        status="draft"
    ).order_by("-created_at")

    return render(request, "blog/drafts.html", {"draft_posts": draft_posts})


@login_required
def publish_post(request, id):
    post = get_object_or_404(Blog, id=id, author=request.user)
    post.status = "published"
    post.save()
    return redirect("post_detail", id=post.id)


