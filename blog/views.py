from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm
from django.db.models import Q, Count
from django.contrib import messages

from blog.models import Post, Category, Tag

def post_create(request):
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Пост создан')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request,
                  'blog/post_form.html',
                  context = {'form':form,
                             'title': 'Новый год'})

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author', 'category').prefetch_related('tags', 'likes'),pk=pk,)
    return render(request, 'blog/post_detail.html', context={'post': post})

def post_list(request):
    """
     главная страница со списком постов
    поиск по загаловку и тексту
    фильтрация по автору, категории и тегу
    сортировка по дате, заголовку и количеству лайков

    """
    # select_related(поля ForeignKey)
    # кзуауеср_кудфеув(поля ManyToMany)
    posts = Post.objects.select_related('author', 'category').prefetch_related('tags', 'likes')
    # получаем из форм ввода HTML в GET запросе

    query = request.GET.get('q', '').strip()
    author_id = request.GET.get('author', '')
    category_id = request.GET.get('category', '')
    tag_id = request.GET.get('tag', '')
    sort = request.GET.get('sort', '-created_at')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(text__icontains=query))

    if author_id:
        posts = posts.filter(author_id=author_id)

    if category_id:
        posts = posts.filter(category_id=category_id)

    if tag_id:
        posts = posts.filter(tag__id=tag_id)

    # annotate добавляет к каждому посту вычисленное поле likes_count
    # по нему можно отсортировать список

    posts = posts.annotate(like_count = Count('likes'))
    allowed_sort_fields = {
        '-created_at': '-created_at',
        'created_at': 'created_at',
        'title': 'title',
        '-likes': '-likes_count',
        'likes': 'likes_count'
    }
    posts = posts.order_by(allowed_sort_fields.get(sort), '-created_at')
    context = {
        'posts': posts,
        'query': query,
        'categories': Category.objects.all(),
        'authors': get_user_model().objects.all().order_by('username'),
        'tags': Tag.objects.all(),
        'select_author': category_id,
        'selected_tag': tag_id,
        'selected_sort': sort
    }
    return render(request, template_name='blog/post_list.html', context=context)