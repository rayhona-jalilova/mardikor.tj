from django import forms
from .models import Xizmat, Kategoriya
from .models import Sharh
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']


class XizmatForm(forms.ModelForm):
    class Meta:
        model = Xizmat
        fields = ['nomi', 'tavsif', 'narx', 'joylashuv', 'telefon', 'rasm', 'kategoriya', 'skidka']
        widgets = {
            'nomi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Масалан: Сантехник'
            }),
            'tavsif': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Маълумоти кӯтоҳ дар бораи хидмат'
            }),
            'narx': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Масалан: 150000'
            }),
            'joylashuv': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Шаҳр ё маҳалла'
            }),
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+992 90 123 4567'
            }),
            'rasm': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'kategoriya': forms.Select(attrs={
                'class': 'form-control'
            }),
            'skidka': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(XizmatForm, self).__init__(*args, **kwargs)
        self.fields['kategoriya'].queryset = Kategoriya.objects.all()


class SharhForm(forms.ModelForm):
    class Meta:
        model = Sharh
        fields = ['matn', 'baho']
        widgets = {
            'matn': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Изоҳ диҳед...'}),
            'baho': forms.Select()
        }
