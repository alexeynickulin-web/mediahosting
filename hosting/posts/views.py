from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Post


def home_view(request, *args, **kwargs):
    post_queryset = Post.objects.all()
    context = {
        "post_queryset": post_queryset
    }
    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)


def post_detail_view(request, id=None):
    post_obj = None
    if id is not None:
        post_obj = Post.objects.get(id=id)
    context = {
        "object": post_obj,
    }

    return render(request, "posts/detail.html", context=context)


def post_search_view(request):
    query_dict = request.GET
    query = query_dict.get('q')
    post_obj = None
    if query is not None:
        post_obj = Post.objects.get(id=query)
    context = {
        "object": post_obj,
    }
    return render(request, "posts/search.html", context=context)
