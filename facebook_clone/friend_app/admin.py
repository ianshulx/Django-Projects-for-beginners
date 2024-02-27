from django.contrib import admin
from .models import FriendsList, FriendRequest
# Register your models here.



class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendsList
admin.site.register(FriendsList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'reciever']
    list_display = ['sender', 'reciever']
    search_fields = ['sender__username', 'sender__email', 'reciever__email', 'reciever__username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)
