from django.db import models
from decimal import Decimal, getcontext
from django.db.models import Avg
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']


class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/no_image.png')
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            self.price = self.price * Decimal(1 - self.discount / 100)
        return Decimal(f'{self.price}').quantize(Decimal('0.00'))

    @property
    def comment_rating(self):
        products = self.comments.aggregate(product_avg_rating=Avg('rating'))
        if products['product_avg_rating'] is None:
            return 0
        return Decimal(f'{products['product_avg_rating']}').quantize(Decimal('0.000'))

    @property
    def get_absolute_url(self):
        return self.image.url

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        ordering = ['my_order']


class Comment(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email} => {self.rating} => {self.product.name}'


class Order(BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField(region='UZ')
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.phone} - {self.product.name}'
