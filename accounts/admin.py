from django.contrib import admin
from .models import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'date_joined')
    search_fields = ['email', 'username']
    list_filter = ('is_active',)
    list_editable = ('is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'department', 'designation', 'joining_date')
    search_fields = ['user__email', 'user__username', 'department', 'designation']
    list_filter = ('gender', 'department')


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
