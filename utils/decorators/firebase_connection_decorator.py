def update_connection_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.updateConnection()
        return func(self, *args, **kwargs)

    return wrapper
