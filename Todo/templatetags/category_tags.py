from django import template
from Todo.models import Category

register = template.Library()

@register.inclusion_tag('inc/_sideb.html')
def get_category():
    categories = Category.objects.all()
    return {'categories': categories}
