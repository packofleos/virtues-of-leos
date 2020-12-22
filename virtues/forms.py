from django import forms
from django.utils import timezone
from django.core.validators import ValidationError

from .models import TaskHistory

class TaskHistoryForm(forms.ModelForm):
    """A form for creating TaskHistory objects. This form is used to record user's tasks."""

    class Meta:
        model = TaskHistory
        fields = ['date', 'task', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add css classes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': f'{name}-input'})
        # we don't want duplicate tasks
        self.fields['task'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('task')
        if task:
            if cleaned_data.get('amount') > task.max_amount:
                # cannot exceed the task's max_amount
                raise ValidationError(f"Amount cannot be greater than {task}'s max_amount ({task.max_amount}).")
        date = cleaned_data.get('date') 
        if date:
            if  date > timezone.now().date():
                raise ValidationError(f"You cannot add a task in the future.")
