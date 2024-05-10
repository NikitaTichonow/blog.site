from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .import models


class PostSitemap(Sitemap):
    def items(self):
        return models.PostModel.objects.filter(status=models.PostModel.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated

    def priority(self, obj):
        return 0.8

    def changefreq(self, obj):
        return "weekly"

    def location(self, obj):
        return reverse('blog:post_page', args=[obj.pk, obj.slug])


class CategorySitemap(Sitemap):
    def items(self):
        return models.PostModel.objects.filter(status=models.PostModel.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated

    def priority(self, obj):
        return 0.8

    def changefreq(self, obj):
        return "weekly"

    def location(self, obj):
        return reverse('blog:category_page', args=[obj.pk, obj.slug])

