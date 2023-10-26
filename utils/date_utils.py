def timedelta_to_str(delta):
    """
    Converts a timedelta to a human-readable string.

    Args:
    - delta (timedelta): The timedelta object to be converted.

    Returns:
    - str: A string in the format "X h Y min Z s".
    """
    total_seconds = int(delta.total_seconds())  # Getting the total seconds from the timedelta
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formatting the string
    formatted_str = ""
    if hours:
        formatted_str += f"{hours}h "
    if minutes:
        formatted_str += f"{minutes}min "
    if seconds or not formatted_str:  # Ensure we return "0s" if delta is very small
        formatted_str += f"{seconds}s"

    return formatted_str.strip()
