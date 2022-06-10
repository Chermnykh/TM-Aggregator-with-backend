from django.contrib import admin
from .models import Task, StripeCustomer, Profile, Timer

# Register your models here.
admin.site.register(Task)
admin.site.register(StripeCustomer)
admin.site.register(Profile)
admin.site.register(Timer)