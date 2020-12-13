from django.contrib import admin

from .models import DailyTask, TaskHistory

admin.site.register(DailyTask)
admin.site.register(TaskHistory)