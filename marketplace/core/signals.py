from django.contrib.auth.models import User # type: ignore
from .models import ProfileModel
from django.db.models.signals import post_save,post_delete # type: ignore
from django.dispatch import receiver # type: ignore
from vender_center.models import Seller
from .models import Review
from core.models import Product

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)

@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """Update product's average rating when reviews change"""
    product = instance.product
    product.save()