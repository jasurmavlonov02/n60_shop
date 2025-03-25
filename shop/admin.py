from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from shop.models import Product, Category, Comment

# Register your models here.

#
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Comment)

admin.site.unregister(Group)


class ProductInline(admin.StackedInline):
    model = Product


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = ('id', 'title')


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ['id', 'name', 'price', 'image_tag', 'my_order']
    search_fields = ('name', 'description')
    list_filter = ('updated_at', 'category')
    ordering = ('my_order',)

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'
