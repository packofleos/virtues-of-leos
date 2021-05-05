from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_guest(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        guest_group = Group.objects.get(name='guest')
        instance.groups.add(guest_group)
