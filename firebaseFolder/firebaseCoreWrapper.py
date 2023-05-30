class FirebaseWrapper:
    def __init__(self):
        pass

    def __getattribute__(self, name):
        if name == "updateConnection":
            return object.__getattribute__(self, name)

        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith("__"):
            def wrapper(*args, **kwargs):
                self.updateConnection()
                return attr(*args, **kwargs)
            return wrapper
        return attr