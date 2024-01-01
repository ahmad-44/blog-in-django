from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post

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


class SinglePostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post

    #tags are not being passed so pass them like this
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        return context
    

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     # identified_post = Post.objects.get(slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })