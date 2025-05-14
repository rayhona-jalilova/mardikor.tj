from django.db import models
from django.contrib.auth.models import User
from django import forms
from decimal import Decimal

class Availability(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)  # xizmat ko‘rsatuvchi
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.provider.username} - {self.date} ({self.start_time} - {self.end_time})"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"




    

class Xizmat(models.Model):
    CATEGORY_CHOICES = [
    ('Сантехник', 'Сантехник'),
    ('Қассоб', 'Қассоб'),
    ('Тозакунанда', 'Тозакунанда'),
    ('Барқчӣ', 'Барқчӣ'),
    ('Ҳашарчӣ', 'Ҳашарчӣ'),
    # add other categories here
]
    
    NOHIYA_TANLOVI = [
    ('Dushanbe', 'Душанбе'),
    ('Khujand', 'Хуҷанд'),
    ('Kulob', 'Кӯлоб'),
    ('Bokhtar', 'Бохтар'),
    ('Hisor', 'Ҳисор'),
    ('Istaravshan', 'Истаравшан'),
    ('Panjakent', 'Панҷакент'),
    ('Tursunzoda', 'Турсунзода'),
    ('Khorugh', 'Хоруғ'),
    ('Other', 'Дигар'),
]

    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    narx = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    telefon = models.CharField(max_length=50, blank=True, null=True)
    nohiya = models.CharField(max_length=50, choices=NOHIYA_TANLOVI, default='Other')
    rasm = models.ImageField(upload_to='xizmatlar_rasmlar/', blank=True, null=True)
    sana = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    kategoriya = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True, default='Дигар')
    skidka = models.BooleanField(default=False)  # YANGI QO‘SHILDI





@property
def narx_skidka_bilan(self):
    if self.skidka:
        return self.narx * (Decimal(1) - (Decimal(self.skidka) / Decimal(100)))
    return self.narx



class Sharh(models.Model):
    matn = models.TextField()
    baho = models.IntegerField()
    sana = models.DateTimeField(auto_now_add=True)
    xizmat = models.ForeignKey(Xizmat, on_delete=models.CASCADE, related_name='sharhlar')  # related_name qo‘shildi
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sharh by {self.foydalanuvchi.username}"

class SharhForm(forms.ModelForm):
    class Meta:
        model = Sharh
        fields = ['baho', 'matn']

class Kategoriya(models.Model):
    nomi = models.CharField(max_length=100)

    def __str__(self):
        return self.nomi