from django import template
register = template.Library()

@register.filter
def obfuscate(email):
    return ''.join(f'&#{ord(char)};' for char in email)

@register.filter
def obfuscate_phone(phone):
    return ''.join(f'&#{ord(char)};' for char in phone)