from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Return dictionary[key] if possible, otherwise None.
    Works with dicts and objects supporting __getitem__ or get().
    """
    try:
        if hasattr(dictionary, "get"):
            return dictionary.get(key)
        return dictionary[key]
    except Exception:
        return None

