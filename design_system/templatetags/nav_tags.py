from django import template

register = template.Library()


@register.inclusion_tag("components/navbar/nav-item.html")
def nav_link(link: str, text: str):
    return {
        'link': link,
        'text': text
    }
