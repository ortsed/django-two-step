from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models import User as User_Extended
from django.contrib.auth.models import User


class UserInline(admin.StackedInline):
	model = User_Extended
	can_delete = False
	verbose_name_plural = 'User'

class UserAdmin(UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
