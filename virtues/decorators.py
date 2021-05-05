from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.contrib import messages

def ignoreUNSAFE_from(groups, redirect_to):
    """Redirects to the provided url of the user has certain group and made an unsafe request.

    groups: Sequence
        The groups to ignore the unsafe request from. Staffs and SuperUsers are immune to this.
    redirect_to: str
        The link to redirect to
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.method in ['POST', 'PUT', 'DELETE']:
                query_condition = Q()
                for group in groups:
                    # chain arbitary OR queries
                    query_condition |= Q(name__exact=group)

                user = request.user
                # user has the group which is to be ignored and made an unsafe request
                if not user.is_staff and not user.is_superuser and user.groups.filter(query_condition):
                    messages.warning(
                        request, f"Post by '{', '.join(groups)}' will be ignored. Contact admin for approval."
                    )
                    return redirect(redirect_to)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator