from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import PostCreateForm, UserlikeForm, SearchForm, CommentForm


def home(request):
	object_list = Post.published.all()
	context = get_context(request, object_list)

	return render(request, 'home.html', context)


def about(request):
	return render(request, 'about.html')


@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
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
	comment_form = CommentForm()
	context = {
		'comment_form': comment_form,
		'post': post}

	return render(request, 'blog/post-detail.html', context)


def category_detail(request, slug):
	category = get_object_or_404(Category, slug=slug)
	object_list = Post.objects.filter(category = category)
	context = get_context(request, object_list)
	context['category'] = category

	return render(request, 'home.html', context)


@login_required
def update_like(request):
	data = {}
	user = request.user
	if user.is_authenticated:
		data['is_valid'] = True
		id = request.GET.get('id')
		post = get_object_or_404(Post, id=id)
		exit_user = post.user_like.filter(username=user.username).exists()
		if exit_user:
			post.user_like.remove(user)
		else:
			post.user_like.add(user)
		data['like_html'] = render_to_string('blog/includes/like-html.html', {'post': post}, request=request)
		
	else:
		data['is_valid'] = False

	return JsonResponse(data)


def post_search(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			posts = Post.objects.filter(Q(body__contains=query) | Q(title__contains=query))

			return render(request, 'blog/search.html', {'posts': posts})
	else:
		form = SearchForm()

	return render(request, 'blog/search.html', {'form': form})


def get_context(request, object_list):
	paginator = Paginator(object_list, 5) 
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	like_form = UserlikeForm()

	return {'posts': posts, 'like_form': like_form}


@login_required
def comment_create(request, slug):
	data = {}
	post = get_object_or_404(Post, slug=slug)
	if request.method == "POST":
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.post = post
			comment.user = request.user
			comment.save()
			data['html_comment'] = render_to_string('blog/includes/comment-list.html', {'post': post}, request=request)

	else:
		comment_form = CommentForm()
	
	context = {
		'post': post,
		'comment_form': comment_form}

	data['html_comment_form'] = render_to_string(
				'blog/includes/html-comment-form.html',
				context,
				request=request)

	return JsonResponse(data)


@login_required
def comment_reply(request, id):
	data = {}
	comment = get_object_or_404(Comment, id=id)
	if request.method == 'POST':
		reply_form = CommentForm(request.POST)
		if reply_form.is_valid():
			reply = reply_form.save(commit=False)
			reply.post = comment.post
			reply.user = request.user
			reply.save()
			comment.replies.add(reply)
			data['html_replies'] = render_to_string(
						'blog/includes/replies.html',
						{'comment': comment},
						request=request)

	else:
		reply_form = CommentForm()

	data['html_reply_form'] = render_to_string(
				'blog/includes/html-reply-form.html',
				{'reply_form': reply_form, 'comment': comment},
				request=request)
	
	return JsonResponse(data)