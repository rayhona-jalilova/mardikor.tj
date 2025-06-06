from django.contrib import admin
from .models import Xizmat

from .models import Sharh

from .models import Availability, Message

admin.site.register(Availability)
admin.site.register(Message)

admin.site.register(Sharh)


class XizmatAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kategoriya', 'narx', 'nohiya', 'telefon', 'sana', 'skidka')
    list_filter = ('kategoriya', 'sana')
    search_fields = ('nomi', 'tavsif', 'nohiya')

admin.site.register(Xizmat, XizmatAdmin)