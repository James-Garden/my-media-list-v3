from django import template
from django.contrib.messages.storage.base import Message

register = template.Library()


@register.inclusion_tag("partials/messages.html")
def render_messages(messages):
    processed_messages = []
    for message in messages:
        processed_messages.append(process_message(message))
    print(processed_messages)
    return {
        'messages': processed_messages
    }


def process_message(message: Message) -> (str, str):
    valid_classes = {'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'}
    message = message.message
    if message[0] == "!":
        for valid_class in valid_classes:
            if message[1: len(valid_class) + 1] == valid_class:
                message = message[len(valid_class) + 1:]
                return message.strip(), valid_class
    return message, 'primary'
