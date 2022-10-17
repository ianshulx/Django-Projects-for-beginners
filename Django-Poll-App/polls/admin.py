from django.contrib import admin
from .models import Poll, Choice, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["text", "owner", "pub_date", "active"]
    search_fields = ["text", "owner__username"]
    list_filter = ["active"]
    date_hierarchy = "pub_date"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "poll"]
    search_fields = ["choice_text", "poll__text"]
    autocomplete_fields = ["poll"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user"]
    search_fields = ["choice__choice_text", "poll__text", "user__username"]
    autocomplete_fields = ["choice", "poll", "user"]
