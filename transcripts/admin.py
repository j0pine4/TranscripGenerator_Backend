from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Document)
admin.site.register(models.Conversation)
admin.site.register(models.Message)
admin.site.register(models.MessageTest)
admin.site.register(models.DailyTokenCount)