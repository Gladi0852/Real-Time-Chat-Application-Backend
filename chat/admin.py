from django.contrib import admin

# Register your models here.

from django.contrib import admin
from chat.models import ChatModel

admin.site.register(ChatModel)