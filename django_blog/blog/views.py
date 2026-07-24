# pyrefly: ignore [missing-import]
# pyrefly: ignore [parse-error]
from .models import Blog
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from .forms import BlogForm



def login_view(request):

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
            return HttpResponse("Invalid Username or Password")

    return render(request, "blog/login.html")


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect("home")

        else:
            return HttpResponse("Passwords do not match")

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

def post_detail(request, id):

    post = get_object_or_404(
        Blog,
        id=id,
        status="published"
    )

    context = {
        "post": post
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )
