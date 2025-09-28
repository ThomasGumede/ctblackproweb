from django.contrib import admin
from home.models import Blog, BlogCategory, Media, EmailModel, Member, ClubFile

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(EmailModel)
class EmailModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

@admin.register(ClubFile)
class ClubFileAdmin(admin.ModelAdmin):
    pass