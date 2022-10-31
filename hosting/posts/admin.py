from django.contrib import admin

from .models import Post, PostAudio, PostDocument, PostImage, PostVideo


class PostAudioInline(admin.StackedInline):
    model = PostAudio
    extra = 0


class PostDocumentInline(admin.StackedInline):
    model = PostDocument
    extra = 0


class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 0


class PostVideoInline(admin.StackedInline):
    model = PostVideo
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostAudioInline,
        PostDocumentInline,
        PostImageInline,
        PostVideoInline
    ]
    list_display = ['title', 'slug', 'user', 'timestamp', 'updated']
    readonly_fields = ['timestamp', 'updated']
    search_fields = ['title', 'content']
    raw_id_fields = ['user']


admin.site.register(PostAudio)
admin.site.register(PostDocument)
admin.site.register(PostImage)
admin.site.register(PostVideo)
admin.site.register(Post, PostAdmin)
