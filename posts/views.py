from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Post, Like
from .forms import PostForm, CommentForm


@login_required
def feed_view(request):
    posts = Post.objects.all()
    return render(request, 'posts/feed.html', {'posts': posts})


@login_required
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    
    else:
        form = PostForm()
        return render(request, 'posts/post.html', {'form':form})



@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # if already liked, unlike it
    return HttpResponseRedirect(f"{request.META.get('HTTP_REFERER')}#post-{post_id}")


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return HttpResponseRedirect(f"{request.META.get('HTTP_REFERER')}#post-{post_id}")
