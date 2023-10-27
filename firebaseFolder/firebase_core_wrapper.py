class FirebaseWrapper:
    def __init__(self):
        pass

    def __getattribute__(self, name):
        if name in ["updateConnection", "_load_cache"]:  # Exclude _load_cache from wrapping
            return object.__getattribute__(self, name)

        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith("__") and not name.startswith("_"):  # Exclude methods that start with '_'
            def wrapper(*args, **kwargs):
                self.updateConnection()
                return attr(*args, **kwargs)  # Removed explicit self, since it's already part of *args
            return wrapper
        return attr