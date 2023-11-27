from django import forms
from django.core.exceptions import ValidationError

from .models import News


class NewsForm(forms.ModelForm):
    text = forms.CharField(min_length=5)
    class Meta:
        model = News
        fields = ['title', 'text', 'category',]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 5:
            raise ValidationError({
                "description": "Описание не может быть менее 20 символов."
            })

        title = cleaned_data.get("name")
        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data