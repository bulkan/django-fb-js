""" This code is from https://github.com/jgorset/fandjango
"""

from datetime import timedelta
from functools import wraps

from django.core.cache import cache

def cached_property(**kwargs):
    """Cache the return value of a property."""
    def decorator(function):
        @wraps(function)
        def wrapper(self):
            key = 'fb_js.%(model)s.%(property)s_%(pk)s' % {
                'model': self.__class__.__name__,
                'pk': self.pk,
                'property': function.__name__
            }

            cached_value = cache.get(key)

            delta = timedelta(**kwargs)

            if cached_value is None:
                value = function(self)
                cache.set(key, value, delta.days * 86400 + delta.seconds)
            else:
                value = cached_value

            return value
        return wrapper
    return decorator
