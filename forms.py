from django import forms
from twilio.rest import TwilioRestClient
from django.conf import settings
from .models import User
from .otp import get_otp_code
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


account = settings.TWILIO_ACCOUNT
token = settings.TWILIO_TOKEN
sender_phone_number = settings.TWILIO_PHONE_NUMBER



class OTPForm1(AuthenticationForm):

	def cleanx(self, *args, **kwargs):
		username = self.cleaned_data.get("username")

		try:
			user = User.objects.get(user__username=username)
			if not user.sms_number:
				raise ValidationError("No user SMS number defined1")
		except User.DoesNotExist:
			raise ValidationError("No user SMS number defined2")

		# Create passcode and send via Twilio
		otp_code = get_otp_code()
		import pdb;pdb.set_trace()
		self.request.session['otp_code'] = otp_code

		try:
			client = TwilioRestClient(account, token)
			client.messages.create(to=user.sms_number, from_=sender_phone_number, body="FusionGPS two-step validation key is %s" % otp_code)
		except: 
			raise Exception("Unable to send SMS")

		messages.add_message(self.data, messages.INFO, 'An SMS message has just been sent to the phone number on file. Enter the code received in the box below to login.')

		return super(OTPForm1, self).clean(*args, **kwargs)


class OTPForm2(forms.Form):
	otp_code = forms.CharField(max_length=255)
	
#	def __init__(self, *args, **kwargs):
#		self.request = kwargs.pop('data', None)
#		return super(OTPForm2, self).__init__(*args, **kwargs)

#	def clean(self):
#		if self.data.session['otp_code'] != self.data['otp_code']:
#			raise forms.ValidationError("Invalid validation code")
#		else:
#			return super(OTPForm2, self).clean(*args, **kwargs)


	
