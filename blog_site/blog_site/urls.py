from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from blog.sitemap import PostSitemap, CategorySitemap
from django.urls import path, include, re_path
from django.views.static import serve


sitemaps = {
    'PostSitemap': PostSitemap,
    'CategorySitemap': CategorySitemap,
}

urlpatterns = [
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'.txt$', serve, {'document_root': settings.STATIC_ROOT, 'path': "robots.txt"}),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)