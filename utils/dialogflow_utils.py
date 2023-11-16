from api_config.object_factory import menuHandler, dialogflowConnectionManager
from dialogflowFolder.dialogflow_session import DialogflowSession


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


def create_dialogflow_session(ip_address: str) -> DialogflowSession:
    """
    Creates and initializes a Dialogflow session.

    Args:
    - ip_address: The IP address to create a session for.

    Returns:
    - A DialogflowSession instance.
    """
    user_instance: DialogflowSession = dialogflowConnectionManager.get_dialogflow_instance(ip_address)
    user_instance.initialize_session(ip_address)
    return user_instance


def get_bot_response_from_session(session: DialogflowSession, user_message: str) -> str:
    """
    Gets the bot response for a given message using an existing Dialogflow session.

    Args:
    - session: An instance of DialogflowSession.
    - user_message: The message from the user.

    Returns:
    - A string containing the bot's response.
    """
    response = session.getDialogFlowResponse(message=user_message)
    bot_answer: str = response.query_result.fulfillment_text
    return bot_answer
