from django.contrib import admin

from .models import DailyTask, TaskHistory, Title

admin.site.register(DailyTask)
admin.site.register(TaskHistory)
admin.site.register(Title)