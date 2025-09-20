from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import UserProfile, Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'word_count', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('created_at',)
    readonly_fields = ('word_count', 'created_at', 'updated_at')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    add_fieldsets = (
        (None, {'classes': ('wide',), 
                'fields': ('email', 'password1', 'password2')}),
    )
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Article, ArticleAdmin)
