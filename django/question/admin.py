from django.contrib import admin
from .models import Subject, Question, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # 4 options per question by default

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'grade', 'text')
    inlines = [OptionInline]

admin.site.register(Subject)
admin.site.register(Question, QuestionAdmin)
