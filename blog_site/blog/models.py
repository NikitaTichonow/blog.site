import random

from django.db import models
from django.urls import reverse
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.utils import timezone


class PostFilesModel(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Имя файла')
    file = models.FileField(upload_to='post_files/')
    code = models.IntegerField(default=0,
                               verbose_name='Код файла',
                               unique=True)
    download_count = models.IntegerField(default=0,
                                         verbose_name='Скачиваний')



    class Meta:
        verbose_name = 'Файл поста'
        verbose_name_plural = 'Файлы постов'

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    import random

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        code = random.randint(100000, 999999)
        while PostFilesModel.objects.filter(code=code).exists():
            code = random.randint(100000, 999999)
        return code

    def __str__(self):
        return self.title


class BotUserModel(models.Model):
    chat_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последняя активность')
    objects = models.Manager()

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

    def __str__(self):
        return self.first_name


class CategoryModel(MPTTModel):
    title = models.CharField(max_length=100,
                             verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Альт. заголовок")
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True,
                            verbose_name='Родительская категория')
    description = models.CharField(max_length=350,
                                   verbose_name="Описание",
                                   blank=True)

    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = 'parent', 'slug'
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'

    def get_absolute_url(self):
        return reverse('blog:category_page', args=[int(self.pk), str(self.slug)])

    def __str__(self):
        return self.title





class PostModel(models.Model):
    """Модель поста"""

    class Status(models.TextChoices):
        """Класс выбора статуса поста"""
        DRAFT = 'ЧЕ', 'Черновик'
        PUBLISHED = 'ОП', 'Опубликовано'

    title = models.CharField(max_length=200,
                             verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Альт. заголовок")
    image = models.ImageField(upload_to='post/%Y/%m/%d',
                              default='default/not_found.png',
                              verbose_name='Изображение поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post',
                               verbose_name="Автор")
    category = TreeForeignKey('CategoryModel',
                              on_delete=models.PROTECT,
                              related_name='post',
                              verbose_name='Категория')
    short_body = CKEditor5Field(max_length=350,
                                verbose_name="Краткое описание",
                                blank=True)
    full_body = CKEditor5Field(verbose_name='Содержимое поста')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name="Опубликовано")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Обновлено")
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name="Статус")
    views = models.IntegerField(default=0,
                                verbose_name="Количество просмотров")

    objects = models.Manager()

    file = models.OneToOneField(PostFilesModel,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             verbose_name="Файл",
                             related_name="post")

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        """Метод получения URL-адреса объекта"""
        return reverse('blog:post_page', args=[int(self.pk), str(self.slug)])

    def get_next_post(self):
        """Метод получения следующего поста"""
        try:
            return self.get_next_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def get_previous_post(self):
        """Метод получения предыдущего поста"""
        try:
            return self.get_previous_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def __str__(self):
        return self.title