from functools import wraps


def dekorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func() + "two"
    return wrapper

@dekorator
def one():
    return "one"

print(one())
print(one.__name__)