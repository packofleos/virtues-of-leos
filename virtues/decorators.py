from django.db.models import Q
from django.shortcuts import redirect, reverse

def ignorePOST_from(groups, redirect_to):
    """Redirects to the provided url of the user has certain group and made a POST request.

    groups: Sequence
        The groups to ignore the POST request from. Staffs and SuperUsers are immune to this.
    redirect_to: str
        The link to redirect to
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            query_condition = Q()
            for group in groups:
                # chain arbitary OR queries
                query_condition |= Q(name__exact=group)
            # user has the group which is to be ignored and made a post request
            user = request.user
            if (user.groups.filter(query_condition) and request.method == 'POST' 
                and not user.is_superuser and not user.is_staff):
                return redirect(redirect_to)

            return view(request, *args, **kwargs)
        return wrapper
    return decorator