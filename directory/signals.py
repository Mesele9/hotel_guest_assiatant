# directory/signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.db import transaction
from django.dispatch import receiver
from django.core.cache import cache
from .models import Hotel, Policy, Service, LocalAttraction, RoomType

logger = logging.getLogger(__name__)

# Receiver for changes in the Hotel model
@receiver(post_save, sender=Hotel)
@receiver(post_delete, sender=Hotel)
def clear_cache_for_hotel(sender, instance, **kwargs):
    transaction.on_commit(lambda: cache.clear())
    logger.info("Cache cleared due to change in Hotel model.")

# Receiver for changes in Policy, Service, LocalAttraction, and RoomType models
@receiver(post_save, sender=Policy)
@receiver(post_save, sender=Service)
@receiver(post_save, sender=LocalAttraction)
@receiver(post_save, sender=RoomType)
@receiver(post_delete, sender=Policy)
@receiver(post_delete, sender=Service)
@receiver(post_delete, sender=LocalAttraction)
@receiver(post_delete, sender=RoomType)
def clear_cache_for_other_models(sender, instance, **kwargs):
    transaction.on_commit(lambda: cache.clear())
    logger.info(f"Cache cleared due to change in {sender.__name__} model.")
