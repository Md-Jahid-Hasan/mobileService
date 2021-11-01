from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model as User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    duration = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + "-" + str(self.price) + " BDT/" + str(self.duration) + " month"


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + " " + str(self.pk)


class Number(models.Model):
    phone_number = models.CharField(max_length=14, unique=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    user = models.ForeignKey(User(), on_delete=models.CASCADE, related_name="users_number")

    def __str__(self) -> str:
        return self.phone_number + " (" + self.company.name + ")"


class UserSubscription(models.Model):
    user = models.ForeignKey(User(), on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    number = models.ForeignKey(Number, on_delete=models.CASCADE, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    

@receiver(post_save, sender=UserSubscription)
def subscription_handler(sender,instance, **kwargs):
    """After save or make payment a update main user profile"""
    instance.user.subs_plan = instance.plan
    instance.user.save()
    