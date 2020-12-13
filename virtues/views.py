from django.utils import timezone
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import DailyTask, TaskHistory
from .forms import TaskHistoryForm

@login_required
def index(request):
    """View for the index of the app. From here, user posts their tasks."""

    tasks = DailyTask.objects.all()
    date = timezone.now()
    # Set initial date for quality of life, it's changable.
    # Sets initial task to be dynamic and quality of life for user.  
    initial = [{'task': task, 'date': date} for task in tasks]
    TaskHistoryFormSet = modelformset_factory(
        TaskHistory, fields=['date', 'task', 'amount'],
        form=TaskHistoryForm, extra=len(tasks)
    )
    
    if request.method != 'POST':
        formset = TaskHistoryFormSet(queryset=TaskHistory.objects.none(), initial=initial)

    else:
        formset = TaskHistoryFormSet(data=request.POST, initial=initial)
        if formset.is_valid():
            histories = formset.save(commit=False)

            for history in histories:
                history.user = request.user
                # User probably wants to modify their record, if it existed in the past.
                # So, in this case just update. Else, create the record.
                history_, created = TaskHistory.objects.update_or_create(
                    date=history.date, user=history.user, task=history.task,
                    defaults={'amount': history.amount} 
                )
            return redirect('virtues:results')

    context = {'formset': formset}
    return render(request, 'virtues/index.html', {'formset': formset})

@login_required
def results(request):
    """View which deals with showing the leaderboard."""

    week_history = TaskHistory.objects.order_by('-date')[:7]
    leaderboard = {}

    for history in week_history:
        user = str(history.user)
        score = history.task.reward * history.amount
        try:
            leaderboard[user] += score
        except KeyError:
            leaderboard[user] = score

    # sort leaderboard by scores
    leaderboard = dict(sorted(leaderboard.items(), reverse=True, key=lambda item: item[1])) 
    context = {'leaderboard': leaderboard}
    return render(request, 'virtues/results.html', context)
