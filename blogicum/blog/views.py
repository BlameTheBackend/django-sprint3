from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Category, Post


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(
            Q(pub_date__lte=timezone.now())
            & (Q(is_published=True) & Q(category__is_published=True))
        ),
        pk=post_id
    )

    context = {
        'post': post
    }

    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.values(
        'id', 'title', 'description').filter(
            is_published=True,
            slug=category_slug))

    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category=category['id'])

    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, 'blog/category.html', context)
