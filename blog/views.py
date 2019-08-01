from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Post, Category
from .forms import PostCreateForm


def home(request):
	categories = Category.objects.all()
	object_list = Post.published.all()

	paginator = Paginator(object_list, 1) 
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {
		'posts': posts,
		'categories': categories}

	return render(request, 'home.html', context)


def about(request):
	return render(request, 'about.html')


@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
	messages.set_level(request, messages.DEBUG)
	if request.method == 'POST':
		form = PostCreateForm(request.POST, files=request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			
			return redirect('home')
		else:
			if form['title'].errors:
				messages.debug(request, "Tiêu đề bài viết không hợp lệ")
			elif form['image'].errors:
				messages.debug(request, "Ảnh tải lên không hợp lệ")
			elif form['category'].errors:
				messages.debug(request, "Loại bài viết không hợp lệ")
			elif form['body'].errors:
				messages.debug(request, "Nội dung bài viết không hợp lệ")

	else:
		form = PostCreateForm()
	context = {
		'form': form}

	return render(request, 'blog/create-post.html', context)


def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	context = {
		'post': post}

	return render(request, 'blog/post-detail.html', context)
