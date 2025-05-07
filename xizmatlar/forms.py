from django import forms
from .models import Xizmat
from .models import Sharh
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class XizmatForm(forms.ModelForm):
    class Meta:
        model = Xizmat
        fields = ['nomi', 'tavsif', 'narx', 'joylashuv', 'telefon', 'rasm', 'kategoriya']  # Rasmni qo‘shish
        widgets = {
            'tavsif': forms.Textarea(attrs={'rows': 4}),
            'kategoriya': forms.Select(attrs={'class': 'form-control'}),
        }


class SharhForm(forms.ModelForm):
    class Meta:
        model = Sharh
        fields = ['matn', 'baho']
        widgets = {
            'matn': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Изоҳ диҳед...'}),
            'baho': forms.Select()
        }
