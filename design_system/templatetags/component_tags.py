from django import template

register = template.Library()


@register.inclusion_tag("components/alert.html")
def alert(message: str, *, alert_class: str = 'primary', dismissible: bool = False):
    return {
        'message': message,
        'alert_class': alert_class,
        'dismissible': dismissible
    }
