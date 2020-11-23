from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


# Create your views here.


def post_list(request):
    post = Post.objects.filter(
        published_date__lte=timezone.now()).order_by("-published_date")
    return render(request, "blog/post_list.html", {
        "post": post

    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        "post": post
    })


def post_new(request):
    if not request.user.is_authenticated:
        return render(request, "blog/no_session.html", {
            "message": "Necesitas iniciar sesion para ver esta pagina"
        })
        # return HttpResponseRedirect(reverse("post_list"))
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {
            "form": form
        })


def post_edit(request, pk):
    if not request.user.is_authenticated:
        return render(request, "blog/no_session.html", {
            "message": "Necesitas iniciar sesion para ver esta pagina"
        })
        # return HttpResponseRedirect(reverse("post_list"))
    else:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("post_list"))
        else:
            return render(request, "blog/login.html", {
                "message": "Invalid Credentials"
            })

    return render(request, "blog/login.html")
