from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404

from .forms import PostForm, PostImageForm
from .models import Post, PostImage


def home_view(request):
    qs = Post.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "home_view.html", context=context)


def post_search_view(request):
    query = request.GET.get('q')
    qs = Post.objects.search(query=query)
    context = {
        "object_list": qs
    }
    return render(request, "posts/search.html", context=context)


def post_detail_view(request, slug=None):
    post_obj = get_object_or_404(Post, slug=slug)
    context = {
        "object": post_obj,
    }
    return render(request, "posts/detail.html", context=context)


@login_required
def post_create_view(request):
    form = PostForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "posts/create-update.html", context)


@login_required
def post_update_view(request, slug=None):
    obj = get_object_or_404(Post, slug=slug, user=request.user)
    form = PostForm(request.POST or None, instance=obj)
    PostImageFormset = modelformset_factory(
        PostImage, form=PostImageForm, extra=0
    )
    qs = obj.postimage_set.all()
    formset = PostImageFormset(request.POST or None, queryset=qs)
    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            # if child.post is None:
            #     print("Добавлена новая")
            #     child.post = parent
            child.post = parent
            child.save()
        context['message'] = 'Данные сохранены.'

    return render(request, "posts/create-update.html", context)


@login_required
def post_delete_view(request, slug=None):
    obj = get_object_or_404(Post, slug=slug, user=request.user)
    if request.method == "POST":
        obj.delete()
        success_url = "home_view"
        return redirect(success_url)
    context = {
        "object": obj,
    }
    return render(request, "posts/delete.html", context)
