from api_config.object_factory import menuHandler


def structureNewDialogflowContext(contextName: str, lifespan: int = 5):
    """
    Generates a new Dialogflow context structure for webhook calls.

    This function is utilized during webhook interactions to facilitate a change in intent on the Dialogflow servers.
    The generated context structure comprises the context name, its lifespan, and an empty parameters dictionary.

    Parameters:
    - contextName (str): The name of the context to be generated.
    - lifespan (int, optional): The lifespan of the context in terms of how many conversational turns it should last.
                                Defaults to 5.

    Returns:
    - list[dict]: A list containing a dictionary with the structured context.

    Example:
    >>> structureNewDialogflowContext("sampleContext", 3)
    [{"name": "baseContextName/contexts/sampleContext", "lifespanCount": 3, "parameters": {}}]

    Note:
    The function relies on a globally accessed 'menuHandler' object with a 'params' dictionary containing
    the base context name ('baseContextName').
    """
    baseContextName = menuHandler.params["baseContextName"]
    newContext = {
        "name": f"{baseContextName}/contexts/{contextName}",
        "lifespanCount": lifespan,
        "parameters": {}
    }
    return [newContext]
