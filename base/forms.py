from django import forms
from .models import Tasks

class TaskImageForm(forms.ModelForm):
    
    class Meta:
        model = Tasks
        fields = ['image']


class ApproveForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['approved']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name','location','assigned','category', 'coins']