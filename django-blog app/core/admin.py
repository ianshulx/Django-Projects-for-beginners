from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title',)
    # this create the slug field from the title field
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)


admin.site.register(Post, PostAdmin)

# TagAdmin must define "search_fields", because it's referenced by PostAdmin.autocomplete_fields.


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
