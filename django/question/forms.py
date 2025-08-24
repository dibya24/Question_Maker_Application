from django import forms
from .models import Question, Option  # Make sure Option model exists

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'grade', 'text', 'status']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question', 'text', 'is_correct']
