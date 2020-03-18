from django.contrib import admin
from .models import Profile
from .models import Worker

class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'skill', 'image')
    list_filter  = ('status', 'created', 'dob')
    search_fields = ('name', 'skill')
    prepopulated_fields = {'slug': ('name',)}

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')

admin.site.register(Worker, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
