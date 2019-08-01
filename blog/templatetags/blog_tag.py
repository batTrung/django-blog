from django import template
from ..models import Post, Category
from django.db.models import Q


register = template.Library()


dict_time = {'days':'ngày', 'day':'ngày', 'hours':'giờ', 'hour':'giờ', 'minutes':'phút', 'minute':'phút', 'weeks':'tuần', 'week':'tuần', 'months':'tháng', 'month':'tháng',"years":"năm",'year':"năm"}
@register.filter
def to_time(value):
	value = str(value)
	result = ''
	for anh, viet in dict_time.items():
		result = value.replace(anh, viet)
		value = result
		
	return result


@register.inclusion_tag('blog/category-list.html')
def get_category():
	return {'categories': Category.objects.all()}
	
