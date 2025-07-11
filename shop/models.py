# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        r = reverse('shop:product_list_by_category',
                       args=[self.slug])
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    # category = models.ForeignKey(Category,
    #                              related_name='products')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    if settings.USE_S3:
        image = models.ImageField(upload_to='products/%Y/%m/%d',
                                  blank=True,
                                  default='products/default.png')
    else:
        image = models.ImageField(upload_to='products/%Y/%m/%d',
                                  blank=True,
                                  default='products/default.png')
        
    # image = models.ImageField(upload_to='products/%Y/%m/%d',
    #                           blank=True)
    description = models.TextField(blank=True)
    # 台灣價錢都是整數，所以可以設定 decimal_places=0
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        r = reverse('shop:product_detail',
                       args=[self.id, self.slug])
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
