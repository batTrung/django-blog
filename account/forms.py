from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class PhotoEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('photo', )


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('name', 'job', 'description', )


class UserRegistrationForm(forms.ModelForm):
	email = forms.CharField(label="email", widget=forms.EmailInput())
	password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Nhập lại mật khẩu", widget=forms.PasswordInput)

	class Meta:
		model = User 
		fields = ('username', 'email', 'password', 'password2', )

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Mật khẩu không khớp.")

		return cd['password2']


