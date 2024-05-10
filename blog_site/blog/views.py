from django.shortcuts import render
from .import models


def index(request):
        categories_list = models.CategoryModel.objects.all()

        context = {
            'categories_list': categories_list,
        }

        return render(request,
                      'blog/index.html',
                      context)


def category_page(request, pk, slug):
    category = models.CategoryModel.objects.get(pk=pk)
    descendant_categories = category.get_descendants(include_self=True)
    posts = models.PostModel.objects.filter(category__in=descendant_categories)

    context = {
        'category': category,
        'posts': posts,
    }

    return render(request,
                  'blog/category_page.html',
                  context)




def post_page(request, pk, slug):
    post = models.PostModel.objects.get(pk=pk)
    post.views += 1
    post.save()

    context = {
        'post': post,
    }

    return render(request,
                  'blog/post_page.html',
                  context)