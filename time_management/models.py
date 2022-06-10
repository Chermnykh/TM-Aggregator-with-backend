from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["complete"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def  __str__(self):
        return f'{self.user.username} Profile'


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Timer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    timer_time_1 = models.IntegerField(default=10)
    timer_time_2 = models.IntegerField(default=10)
    timer_time_3 = models.IntegerField(default=10)
    timer_time_4 = models.IntegerField(default=10)
    timer_time_5 = models.IntegerField(default=10)
    timer_time_6 = models.IntegerField(default=10)
    timer_time_7 = models.IntegerField(default=10)
    timer_time_8 = models.IntegerField(default=10)
    timer_time_max_1 = models.IntegerField(default=10)
    timer_time_max_2 = models.IntegerField(default=10)
    timer_time_max_3 = models.IntegerField(default=10)
    timer_time_max_4 = models.IntegerField(default=10)
    timer_time_max_5 = models.IntegerField(default=10)
    timer_time_max_6 = models.IntegerField(default=10)
    timer_time_max_7 = models.IntegerField(default=10)
    timer_time_max_8 = models.IntegerField(default=10)
    def __str__(self):
        return str(self.timer_time_1)

