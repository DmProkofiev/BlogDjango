from email import message

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm
from django.db.models import Q, Count
from django.contrib import messages
from blog.models import Post, Category, Tag

@login_required
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
    return render(request,'blog/post_create.html',context = {'form':form})

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
    posts = Post.objects.select_related('author', 'category').prefetch_related('tags', 'likes')

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
        posts = posts.filter(tags__id=tag_id)

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
    posts = posts.order_by(allowed_sort_fields.get(sort, '-created_at'))
    context = {
        'posts': posts,
        'query': query,
        'categories': Category.objects.all(),
        'authors': get_user_model().objects.all().order_by('username'),
        'tags': Tag.objects.all(),
        'select_author': category_id,
        'selected_tag': tag_id,
        'selected_sort': sort,
        'page_heading': 'Посты пользавателя',
        'page_description':'Читайте посты, ищите по тексту, фильтруйте по автору, категории и тегам'
    }
    return render(request, template_name='blog/post_list.html', context=context)

def user_posts(request, user_id):
    """
    просмотр постов любого пользавателя
    user_id приходит из адреса страницы
    """
    author = get_object_or_404(get_user_model(), pk=user_id)
    posts = (
        Post.objects.select_related('author', 'category').prefetch_related('tags', 'likes').filter(author=author).annotate(likes_count=Count('likes')).order_by('-created_at')
    )
    context={
        'posts': posts,
        'hide_filters': True,
        'page_heading': f'Посты пользавателя {author.username}',
        'page_description': 'Публичный список постов выбранного автора'
    }
    return render(request, template_name='blog/post_list.html', context=context)

@login_required
def post_update(request, pk):
    post= get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        message.error(request, 'Можно редактировать тольк освои посты')
        return redirect(post)

    if request.method == 'POST':
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
    else:
        form = PostForm(instance=post)
    return render(request, template_name='blog/post_form.html', context={'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'Удалять можно только свои посты')
        return redirect(post)
    if request.method=='POST':
        post.delete()
        messages.success(request, 'Пост удален')
    return redirect('blog:post_list')
