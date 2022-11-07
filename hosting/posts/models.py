from django.conf import settings
import pathlib
import uuid
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

from .utils import slugify_instance_title, transcribe_image

User = settings.AUTH_USER_MODEL


class PostQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Post(models.Model):
    user = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        verbose_name='Слаг'
    )
    content = models.TextField(
        verbose_name='Описание'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )
    publish = models.DateField(
        auto_now_add=False,
        auto_now=False,
        null=True, blank=True,
        verbose_name='Время публикации'
    )
    pub_status = models.BooleanField(
        default=True,
        verbose_name='Статус публикации'
    )

    objects = PostManager()

    def get_absolute_url(self):
        return reverse("post_detail_view", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("post_update_view", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("post_delete_view", kwargs={"slug": self.slug})

    def get_images_children(self):
        return self.postimage_set.all()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


def post_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


pre_save.connect(post_pre_save, sender=Post)


def post_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    if created:
        slugify_instance_title(instance, save=True)


post_save.connect(post_post_save, sender=Post)


def post_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())
    return f"posts/images/{new_fname}{fpath.suffix}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # image = models.FileField(upload_to=post_image_upload_handler)
    name = models.CharField(max_length=250, blank=True)
    transcription = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# def post_image_post_save(sender, instance, created, *args, **kwargs):
#     print('post_image_post_save', instance.image)
#     if created:
#         transcribe_image(instance, save=True)


# post_save.connect(post_image_post_save, sender=PostImage)


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    transcription = models.TextField(blank=True)


class PostAudio(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    transcription = models.TextField(blank=True)


class PostDocument(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    transcription = models.TextField(blank=True)
