from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('target', 'start_date', 'end_date', 'description', 'difficulty_classification', 'status')
    list_filter = ('start_date', 'end_date',)
    prepopulated_fields = {'slug': ('target',)}
    raw_id_fields = ('author',)
    search_fields = ('target',)
    ordering = ('start_date',)




