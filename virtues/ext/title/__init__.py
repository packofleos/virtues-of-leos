from ...models import Title

def set_title(user, overall, per_task):
    """Set/Update user's titles."""
    titles = Title.objects.all()
    for title in titles:
        globals()[f'_set_{title.condition.lower()}'](
            title, 
            user=user,
            overall=overall,
            per_task=per_task,
        )

def _set_highest(title, per_task, **kwargs):
    """Verify users' qualification for Highest score based titles."""
    top_users = set()
    for task in title.tasks.all():
        # reversed sorted dictionary is expected
        top_users.add(list(per_task[str(task)])[0])

    if len(top_users) == 1:
        title.users.remove(title.users.all().first())
        title.users.add(*top_users)

def _set_minimum(title, overall, **kwargs):
    """Verify users' qualification for overall Minimum score based titles."""
    for user in title.users.all():
        if user not in overall:
            title.users.remove(user)

    for user, score in overall.items():
        if score >= title.amount:
            title.users.add(user)
