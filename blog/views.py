from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ['-date']
    context_object_name = "posts"
    def get_queryset(self): # override this funciton
        return super().get_queryset()[:3] #only get 3 latest elements

# Create your views here.
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]  #now django will create a single query and fetch only 3 results. Optimization {Negative indexing is not allowed in the slicing here}
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })


class AllPostView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'



# def posts(request):
#     all_posts = latest_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts
#     })


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id")
        }

        return render(request, "blog/post-detail.html", context)
    

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     # identified_post = Post.objects.get(slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })