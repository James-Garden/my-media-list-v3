from django import template
import urllib.parse

register = template.Library()


@register.inclusion_tag("search/pagination.html", takes_context=True)
def pagination(context):
    path, params = context['request'].path, context['request'].GET.copy()
    page_obj = context['page_obj']
    params.pop("page", None)
    full_path = f"{path}?{urllib.parse.urlencode(params)}"

    return {
        'page_obj': page_obj,
        'full_path': full_path
    }
