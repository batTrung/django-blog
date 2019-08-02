from django import forms 
from .models import Post, Category, Comment


class PostCreateForm(forms.ModelForm):
	category = forms.ModelChoiceField(label="Category", widget=forms.Select, queryset=Category.objects.all())

	class Meta:
		model = Post
		fields = ('title', 'image', 'active', 'category', 'body', )


class SearchForm(forms.Form):
	query = forms.CharField()


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body', )


