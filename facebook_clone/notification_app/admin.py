from django.contrib import admin

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['content_type',]
    list_display = ['target', 'content_type', 'timestamp']
    search_fields = ['target__username',]
    readonly_fields = []

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)
