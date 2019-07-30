from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import Profile
from .forms import LoginForm, UserRegistrationForm


User = get_user_model()


def login(request):
	data = {}

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request,
								username=cd['username'],
								password=cd['password'])
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					data['form_valid'] = True
					data['username'] = user.username
				else:
					data['form_valid'] = False
					data['error'] = 'Tài khoản đã bị vô hiệu hóa'
			else:
				data['form_valid'] = False
				data['error'] = 'Tên hoặc mật khẩu không đúng.'
		else:
			data['form_valid'] = False
			data['error'] = 'Tên hoặc mật khẩu không đúng.'

	else:			
		form = LoginForm()

	html_form = render_to_string(
		'account/login-form.html',
		{'form': form},
		request=request)
	data['html_form'] = html_form

	return JsonResponse(data)


def register(request):
	data = {}
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password'])
			new_user.save()
			Profile.objects.create(user=new_user)
			user = authenticate(request,
								username=request.POST['username'],
								password=request.POST['password'])
			auth_login(request, user)
			data['form_valid'] = True

		else:
			data['form_valid'] = False
			if user_form['username'].errors:
				data['error'] = "Tên không hợp lệ. Tên chỉ chứa các ký tự, số và @/./+/-/_"
				print(user_form['username'].errors)
			elif user_form['email'].errors:
				data['error'] = 'Địa chỉ email không hợp lệ'
			elif user_form['password'].errors:
				print(user_form['password'].errors)
				data['error'] = 'Mật khẩu không hợp lệ. Ít nhất có 8 ký tự.'
			elif user_form['password2'].errors:
				data['error'] = 'Mật khẩu không hợp lệ hoặc không khớp.'

	else:
		user_form = UserRegistrationForm()

	html_form = render_to_string(
					'account/register.html',
					{'form': user_form},
					request=request)
	data['html_form'] = html_form

	return JsonResponse(data)



def profile(request, username):
	user = get_object_or_404(User, username=username)
	context = {
		'user': user}

	return render(request, 'account/profile.html', context)