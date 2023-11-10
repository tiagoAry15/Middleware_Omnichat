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


async def _get_bot_response_from_user_session(user_message: str, ip_address: str) -> str:
    user_instance: DialogflowSession = dialogflowConnectionManager.get_instance_session(ip_address)

    # Inicializa a sessão, assumindo que 'initialize_session' não é uma coroutine
    user_instance.initialize_session(ip_address)

    # Aguarda a resposta da função assíncrona 'getDialogFlowResponse'
    response = await user_instance.getDialogFlowResponse(message=user_message)

    # Extrai o texto da resposta
    bot_answer: str = response.query_result.fulfillment_text

    return bot_answer
