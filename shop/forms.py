from django import forms

from shop.models import Product, Category, Comment, Order
from phonenumber_field.formfields import PhoneNumberField


# Form vs ModelForm

#
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=200)
#     description = forms.CharField(widget=forms.Textarea)
#     price = forms.DecimalField(max_digits=14, decimal_places=2)
#     image = forms.ImageField(required=False)
#     quantity = forms.IntegerField(required=False)
#     category = forms.ModelChoiceField(queryset=Category.objects.all())
#     discount = forms.IntegerField(required=False, min_value=0, max_value=100)
#     rating = forms.ChoiceField(choices=Product.RatingChoice)
#
#     def save(self, commit=True):
#         cd = self.cleaned_data
#         product = None
#         if commit:
#             product = Product.objects.create(
#                 name=cd.get('name'),
#                 description=cd.get('description'),
#                 price=cd.get('price'),
#                 image=cd.get('image'),
#                 quantity=cd.get('quantity'),
#                 category=cd.get('category'),
#                 discount=cd.get('discount'),
#                 rating=cd.get('rating')
#             )
#         return product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product',)


class OrderModelForm(forms.ModelForm):
    phone = PhoneNumberField(region='UZ')

    class Meta:
        model = Order
        exclude = ('product',)
