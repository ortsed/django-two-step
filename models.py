from django.db import models

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
	user = models.OneToOneField(User)
	sms_number = PhoneNumberField()

