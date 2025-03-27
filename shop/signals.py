import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from core.settings import BASE_DIR
from shop.models import Category, Product
from users.models import CustomUser


def create_category(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'Hello Dear!',
            f'Category {instance.title} successfully inserted',
            'jasurmavlonov24@gmail.com',
            [user.email for user in CustomUser.objects.filter(is_superuser=True)]
        )


post_save.connect(create_category, sender=Category)


# Do you understand ?
# [i**2 for i in range(1,101)]


@receiver(pre_delete, sender=Product)
def save_data_before_deleted(sender, instance, **kwargs):
    data = {
        'name': instance.name,
        'description': instance.description,
        'price': float(instance.price),
        'image': str(instance.image.url),
        'discount': instance.discount,
        'quantity': instance.quantity,
        'category': instance.category.id
    }
    file_path = os.path.join(BASE_DIR, 'shop', 'backup', 'product_backup.json')
    if os.path.exists(file_path):
        with open(file_path) as f:
            try:
                product_data = json.load(f)
            except json.JSONDecodeError:
                product_data = []
    else:
        product_data = []
    product_data.append(data)
    with open(file_path, 'w') as f:
        json.dump(product_data, f, indent=4)

    print('Product successfully saved')
