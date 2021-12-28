from django import forms
from django.core.exceptions import ValidationError


class ItemForm(forms.Form):
    chai = forms.IntegerField(required=False)
    apple = forms.IntegerField(required=False)
    coffee = forms.IntegerField(required=False)
    milk = forms.IntegerField(required=False)
    oatmeal = forms.IntegerField(required=False)

    def clean(self):
        data = self.cleaned_data
        for key, value in data.items():
            if isinstance(value, int) and value < 0:
                raise ValidationError(f"Value of {key} must be in positive")
        return data
