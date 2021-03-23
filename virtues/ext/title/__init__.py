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
        try:
            # reversed sorted dictionary is expected so top user for
            # per_task['task name'] is the the first user i.e list(...)[0] 
            top_users.add(list(per_task[str(task)])[0])
        except KeyError:
            # no user submitted a specfic task required by the title
            # So, no one gets gets the title
            top_users.clear()
            break

    title.users.remove(title.users.all().first())
    if len(top_users) == 1:
        title.users.add(*top_users)


def _set_minimum(title, overall, **kwargs):
    """Verify users' qualification for overall Minimum score based titles."""
    for user in title.users.all():
        if user not in overall:
            title.users.remove(user)

    for user, score in overall.items():
        if score >= title.amount:
            title.users.add(user)
        else:
            title.users.remove(user)
