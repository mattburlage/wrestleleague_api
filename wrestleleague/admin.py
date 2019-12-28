from django.contrib import admin
from django import forms

from .models import *


class MatchQuestionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['correct_answer'].queryset = Answer.objects.filter(question__id=self.instance.id)


class MatchQuestionInline(admin.TabularInline):
    model = MatchQuestion
    form = MatchQuestionAdminForm
    fields = ['question', 'correct_answer',]
    show_change_link = True


class EventAdmin(admin.ModelAdmin):
    inlines = [MatchQuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ['answer', 'image_url', 'id']


class MatchQuestionAdmin(admin.ModelAdmin):
    form = MatchQuestionAdminForm
    inlines = [AnswerInline]


admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Event, EventAdmin)
admin.site.register(Promotion)
admin.site.register(MatchQuestion, MatchQuestionAdmin)
admin.site.register(Season)
