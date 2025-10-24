from typing import Callable


def first_non_null(*args):
    for value in args:
        if value is not None:
            return value
    return None


def extract_dict(obj, *names):
    d = {}
    for x in names:
        v = getattr(obj, x)
        d[x] = v() if isinstance(v, Callable) else v
    return d


return_rv_img = dict(_='plugfun', type='img')


def dev_function(dev_return=None):
    """
    Decorator that provides a default return value when running in development mode.
    If the renderer is in dev mode, returns a mock or substituted value.
    """

    def decorator(function):
        def wrapped_call(*kargs, **kwargs):
            from src import RenderGlobals
            if RenderGlobals.renderer.is_dev:

                def get_retval(v):
                    if isinstance(v, dict) and v.get('_') == 'plugfun':
                        if v['type'] == 'img':
                            return RenderGlobals.renderer.rv.img
                    return v

                if isinstance(dev_return, dict):
                    return get_retval(dev_return)
                if isinstance(dev_return, list):
                    return [get_retval(v) for v in dev_return]
                if isinstance(dev_return, tuple):
                    return tuple(get_retval(v) for v in dev_return)
                if callable(dev_return):
                    return get_retval(dev_return(*kargs, **kwargs))
                return dev_return

            return function(*kargs, **kwargs)

        return wrapped_call

    return decorator
