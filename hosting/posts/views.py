from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import PostForm
from .models import Post


def home_view(request, *args, **kwargs):
    post_queryset = Post.objects.all()
    context = {
        "post_queryset": post_queryset
    }
    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)


def post_search_view(request):
    query_dict = request.GET
    try:
        query = int(query_dict.get("q"))
    except:
        query = None
    post_obj = None
    if query is not None:
        post_obj = Post.objects.get(id=query)
    context = {
        "object": post_obj,
    }
    return render(request, "posts/search.html", context=context)


@login_required
def post_create_view(request):
    form = PostForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        post_object = form.save()
        context['form'] = PostForm()
    return render(request, "posts/create.html", context=context)


def post_detail_view(request, id=None):
    post_obj = None
    if id is not None:
        post_obj = Post.objects.get(id=id)
    context = {
        "object": post_obj,
    }

    return render(request, "posts/detail.html", context=context)
