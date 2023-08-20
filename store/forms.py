from django import forms

from store.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["slug"]


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))

    class Meta:
        model = ProductImage
        fields = ["image"]
