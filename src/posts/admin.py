from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'timestamp']
    list_filter = ['updated', 'timestamp']
    list_display_links = ['updated']
    list_editable = ['title']
    search_fields = ['title', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)

"""Note: List_display has many optional options for admin panel and you can use it for your desired requirements"""
