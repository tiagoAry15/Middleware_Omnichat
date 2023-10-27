from functools import wraps


def cache_create(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        result = func(instance, *args, **kwargs)
        if result:  # If creation was successful
            unique_id = instance.firebaseConnection.writeData(data=args[0])  # Assumes speisekarte_data is the first arg
            instance.data[unique_id] = args[0]
            instance.save_cache()
        return result

    return wrapper


def cache_update(func):
    @wraps(func)
    def wrapper(instance, unique_id_value, *args, **kwargs):
        if not args:
            print("No update arguments were provided.")
            return None
        newData = args[0]

        speisekarte = instance.read_speisekarte(unique_id_value)  # Use it as a positional argument
        if not speisekarte:
            print(f"Could not find an element in database tied to {unique_id_value}.")
            return None

        # Call the original function without the unique_id_value argument
        result = func(instance, unique_id_value, newData, **kwargs)

        if result:  # If update was successful
            instance.data[unique_id_value] = speisekarte
            instance.save_cache()
        return result

    return wrapper


def cache_delete(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        result = func(instance, *args, **kwargs)
        if result:  # If delete was successful
            speisekarte_unique_id = instance.get_unique_id_by_author(args[0])  # Assumes author is the first arg
            instance.data.pop(speisekarte_unique_id)
            instance.save_cache()
        return result
    return wrapper
