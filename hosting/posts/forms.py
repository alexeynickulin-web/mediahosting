from django import forms

from .models import Post, PostImage


class PostForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    title = forms.CharField(
        label="Название",
        help_text="Введите название публикации",
        widget=forms.TextInput(
            attrs={
                "label": "Название",
                "placeholder": "Название публикации"
            }
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "class": "form-control"
            }
            self.fields[str(field)].widget.attrs.update(new_data)

    # def clean(self):
    #     data = self.cleaned_data
    #     title = data.get("title")
    #     qs = Post.objects.filter(title__icontains=title)
    #     if qs.exists():
    #         self.add_error(
    #             "title",
    #             f"\"{title}\" is already in use. Please pick another title."
    #         )
    #     return data


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        # fields = ['name', 'image']
        fields = ['name']
