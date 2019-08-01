from django import forms 
from .models import Post, Category


class PostCreateForm(forms.ModelForm):
	category = forms.ModelChoiceField(label="Category", widget=forms.Select, queryset=Category.objects.all())

	class Meta:
		model = Post
		fields = ('title', 'image', 'active', 'category', 'body', )
