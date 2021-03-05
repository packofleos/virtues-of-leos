import datetime

from django.utils import timezone
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from . import app_conf
from .models import DailyTask, TaskHistory, Title
from .forms import TaskHistoryForm
from .decorators import ignorePOST_from

from .ext import title

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
                amount = history.amount
                fields = {'date': history.date, 'user': history.user, 'task': history.task}
                # check for amount because NULL amount shouldn't be stored on the database.
                # don't use 'if amount' because 0s are accepted.
                if amount is not None:
                    # User probably wants to modify their record, if it existed in the past.
                    # So, in this case just update. Else, create the record.
                    if amount == 0:
                        try:
                            TaskHistory.objects.get(**fields).delete()
                        except TaskHistory.DoesNotExist:
                            pass
                    else:
                        TaskHistory.objects.update_or_create(**fields, defaults={'amount': amount})
            return redirect('virtues:results')

    context = {'formset': formset, 'forms_and_tasks': zip(formset, tasks)}
    return render(request, 'virtues/index.html', context)

@login_required
def results(request):
    """View which deals with showing the leaderboard."""

    latest_history = TaskHistory.objects.all()
    # delete old task histories
    latest_history.filter(date__lt=timezone.now()-datetime.timedelta(days=app_conf.MAX_DAY)).delete()
    overall_queryset = TaskHistory.get_score(latest_history)
    per_task_queryset = TaskHistory.get_score(latest_history, per_task=True)

    leaderboard_overall = {User.objects.get(pk=entry['user']): entry['score'] for entry in overall_queryset}

    leaderboard_per_task = {}
    for entry in per_task_queryset:
        per_task = {User.objects.get(pk=entry['user']): entry['score']}
        try:
            leaderboard_per_task[entry['task__name']].update(per_task)
        except KeyError:
            leaderboard_per_task[entry['task__name']] = per_task

    title.set_title(request.user, leaderboard_overall, leaderboard_per_task)
    context = {'leaderboard': leaderboard_overall, 'per_task': leaderboard_per_task}
    return render(request, 'virtues/results.html', context)

@login_required
def show_titles(request):
    titles = Title.objects.all()
    context = {'titles': titles}
    return render(request, 'virtues/titles.html', context)