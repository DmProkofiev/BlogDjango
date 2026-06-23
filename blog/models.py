from django.db import models
from django.conf import settings
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField('название', max_length = 50, unique = True)
    slug = models.SlugField('slug', max_length = 60, unique = True)

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('название', max_length = 80, unique = True)
    slug = models.SlugField('slug', max_length = 90, unique = True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('заголовок', max_length = 200)
    text = models.TextField('текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'posts', verbose_name='автор')
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, blank = True, null = True, related_name = 'категория')
    tags = models.ManyToManyField(Tag, blank = True, related_name = 'posts', verbose_name = 'тэги')

    image1 = models.ImageField('изображение 1', upload_to='posts/', blank = True, null=True)
    image2 = models.ImageField('изображение 2', upload_to='posts/', blank=True, null=True)
    image3 = models.ImageField('изображение 3', upload_to='posts/', blank=True, null=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name = 'liked_posts', verbose_name = 'лайки')

    created_at = models.DateTimeField('создано', auto_now_add = True)
    updated_at = models.DateTimeField('обновлено', auto_now = True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs = {'pk': self.pk})
