import datetime

from django.utils import timezone
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import DailyTask, TaskHistory
from .forms import TaskHistoryForm
from .decorators import ignorePOST_from

@login_required
@ignorePOST_from(['guest'], 'virtues:results')
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
                if history.amount != 0:
                    # User probably wants to modify their record, if it existed in the past.
                    # So, in this case just update. Else, create the record.
                    history_, created = TaskHistory.objects.update_or_create(
                        date=history.date, user=history.user, task=history.task,
                        defaults={'amount': history.amount} 
                    )
            return redirect('virtues:results')

    context = {'formset': formset, 'forms_and_tasks': zip(formset, tasks)}
    return render(request, 'virtues/index.html', context)

@login_required
def results(request):
    """View which deals with showing the leaderboard."""

    week_history = TaskHistory.objects.filter(date__gte=timezone.now()-datetime.timedelta(days=7))
    entries = {entry['user__username']: entry['score'] for entry in TaskHistory.get_score(week_history)}

    # sort leaderboard by scores
    leaderboard = dict(sorted(entries.items(), reverse=True, key=lambda item: item[1])) 
    context = {'leaderboard': leaderboard}
    return render(request, 'virtues/results.html', context)
