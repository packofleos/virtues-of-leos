from django.db import models
from django.db.models import F, Sum
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class DailyTask(models.Model):
    """The model of daily tasks."""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    reward = models.PositiveIntegerField(choices=[(n, n) for n in range(1, 11)])
    max_amount = models.PositiveIntegerField(validators=[MaxValueValidator(1000)])

    def __str__(self):
        return self.name

class TaskHistory(models.Model):
    """The history model of the task completation."""
    class Meta:
        constraints = [
            # no two row or more should have the same date, user and task.
            # since, we either want our user to add their record or update a previous one.
            models.UniqueConstraint(fields=['date', 'user', 'task'], name='unique_user_taskhistory')
        ]

    date = models.DateField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE)
    # amount field cannot exceed task's max_amount and the validation is handled in the model form
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} - {str(self.user)} - {str(self.task)}"

    @classmethod
    def get_score(cls, queryset, per_task=False, sortby_score=True):
        """Get score of users from queryset.

        querset: QuerySet
            The queryset to determine the score from.
        per_task: bool = False
            Returns score per task when True.
        sortby_score: bool = True
            Sort the scores (in descending order) or not. Returns a list instead of queryset when True.
        """
        values = ['user__username']
        if per_task:
            values.append('task__name')

        result = queryset.values(*values).distinct().annotate(score=Sum(F('amount') * F('task__reward')))
        result = sorted(result, reverse=True, key=lambda record: record['score']) if sortby_score else result

        return result