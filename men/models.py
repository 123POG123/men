from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from pytils.translit import slugify as sl

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def user_slugify(s):
    return slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class MenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Men.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('men:category', kwargs={'cat_slug': self.slug})


class Tags(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'

    def get_absolute_url(self):
        return reverse('men:tag', kwargs={'tag_slug': self.slug})


class Men(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Опубликованно'

    title = models.CharField(max_length=200, verbose_name='Заголовок', null=True)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories', verbose_name='Категории')
    description = models.TextField(blank=True, verbose_name='Биография')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Фотография')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tags, blank=True, related_name='tags', verbose_name='Таг')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)
    is_published = models.CharField(max_length=15,
                                    choices=Status.choices,
                                    default=Status.PUBLISHED,
                                    verbose_name='Статус'
                                    )
    data_of_bird = models.DateField(blank=True, null=True, verbose_name='День рождения')
    objects = models.Manager()
    published = MenManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['create']),
        ]

    def get_absolute_url(self):
        return reverse('men:post_detail', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = sl(self.title)
        return super().save(*args, **kwargs)
