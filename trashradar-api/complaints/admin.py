from django.contrib import admin

from complaints.models import Entity


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'twitter', 'created')
    list_edit = ('name', 'twitter', 'phone')
