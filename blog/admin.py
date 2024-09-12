from django.contrib import admin

from blog.models import BlogEntry


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'publications', 'views', 'created_at', 'updated_at')
    search_fields = ('title', 'publications', 'views', 'created_at', 'updated_at')
    list_filter = ('publications', 'views')

# Register your models here.
