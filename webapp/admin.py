from django.contrib import admin

# Register your models here.
from webapp.models import Sketchpad, Status, Type, Project


class SketchpadAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'created_time', 'updated_time']
    list_display_links = ['description']
    list_filter = ['status', 'type']
    search_fields = ['status']
    fields = ['summary', 'description', 'status', 'type', 'created_time', 'updated_time']
    readonly_fields = ['created_time', 'updated_time']


admin.site.register(Sketchpad, SketchpadAdmin)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project)
