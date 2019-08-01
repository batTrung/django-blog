from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm, PhotoForm


User = get_user_model()


def login(request):
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
					next_url = request.POST.get('next')
					if next_url:
						return HttpResponseRedirect(next_url)
					return redirect('home')
				else:
					messages.debug(request, 'Tài khoản đã bị vô hiệu hóa')
		else:
			messages.debug(request, 'Tên hoặc mật khẩu không đúng.')
	else:			
		form = LoginForm()

	return render(request, 'account/login.html', {'form': form})


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
			messages.success(request, 'Đăng ký thành công')
			return redirect('home')
		else:
			if user_form['username'].errors:
				messages.debug(request, 'Tên không hợp lệ. Tên chỉ chứa các ký tự, số và @/./+/-/_')
			elif user_form['email'].errors:
				messages.debug(request, 'Địa chỉ email không hợp lệ')
			elif user_form['password'].errors:
				messages.debug(request, 'Mật khẩu không hợp lệ. Ít nhất có 8 ký tự.')
			elif user_form['password2'].errors:
				messages.debug(request, 'Mật khẩu không hợp lệ hoặc không khớp.')

	else:
		user_form = UserRegistrationForm()


	return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit_profile(request):
	try: 
		profile = request.user.profile
	except:
		profile = None

	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(
			instance=profile,
			data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile = profile_form.save(commit=False)
			profile.user = request.user
			profile.save()
			messages.success(request, 'Cập nhật thành công')
		else:
			messages.debug(request, 'Cập nhật không thành công. Vui lòng thử lại')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=profile)

	context = {
		'user': request.user,
		'user_form': user_form,
		'profile_form': profile_form}

	return render(request, 'account/profile.html', context)


@login_required
def photo_update(request):
	try: 
		profile = request.user.profile
	except:
		profile = None

	if request.method =='POST':
		photo_form = PhotoForm(instance=profile, data=request.POST, files=request.FILES)
		if photo_form.is_valid():
			print(profile.photo.url)
			photo_form.save()
			photo_html = render_to_string('account/includes/photo-form.html', {'user': request.user})

			data = {'is_valid':True, 'photo_html':photo_html}
		else:
			data = {'is_valid':False}

		return JsonResponse(data)