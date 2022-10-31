from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Post.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error(
                "title",
                f"\"{title}\" is already in use. Please pick another title."
            )
        return data
