from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from .forms import OTPForm1, OTPForm2


from django.contrib.auth import authenticate, login


from twilio.rest import TwilioRestClient
from django.conf import settings
from .models import User
from .otp import get_otp_code
from django.contrib import messages
from django.core.exceptions import ValidationError
account = settings.TWILIO_ACCOUNT
token = settings.TWILIO_TOKEN
sender_phone_number = settings.TWILIO_PHONE_NUMBER
from django.contrib.auth.forms import AuthenticationForm

class TwoStepWizardView(SessionWizardView):

	form_list = [OTPForm1, OTPForm2]

	def done(self, form_list, form_dict, **kwargs):
		if ("%s" % self.request.session['otp_code']) != self.request.POST['1-otp_code']:
			raise ValidationError("Invalid validation code")
	        username = form_list[0].data['0-username']
		password = form_list[0].data['0-password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(self.request, user)
				return HttpResponseRedirect('/admin/')

	def process_step(self, form):
		if form.data['two_step_wizard_view-current_step'] == '0':
			try:
				user = User.objects.get(user__username=form.data['0-username'])
				if not user.sms_number:
					raise ValidationError("No user SMS number defined1")
			except User.DoesNotExist:
				raise ValidationError("No user SMS number defined2")

			# Create passcode and send via Twilio
			otp_code = get_otp_code()
			print otp_code
			self.request.session['otp_code'] = otp_code
			try:
				pass
				#client = TwilioRestClient(account, token)
				#client.messages.create(to=user.sms_number.as_international, from_=sender_phone_number, body="FusionGPS two-step validation key is %s" % otp_code)
			except:
				raise Exception("Unable to send SMS")

			messages.add_message(self.request, messages.INFO, 'An SMS message has just been sent to the phone number on file. Enter the code received in the box below to login.')
		
		return super(TwoStepWizardView, self).process_step(form)
