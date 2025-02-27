from django import forms

from shop.models import Product


# Form vs ModelForm


class ProductForm(forms.Form):
    pass


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ()
