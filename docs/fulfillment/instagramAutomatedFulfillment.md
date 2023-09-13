## instagramFulfillmentSetter.py

This module is responsible for updating the webhook callback URL for Instagram integrations. It automates the process of setting a new webhook URL, which is crucial for maintaining the integration between the Instagram platform and your application. Here are the primary functionalities of this module:

- **Fetching the Current ngrok URL**: Utilizes the `get_ngrok_url` function from the `fulfillment.ngrokGetter` module to retrieve the current URL exposed by ngrok.
- **Setting the New Instagram Webhook Callback URL**: The `setNewInstagramWebhookCallbackURL` function, which is decorated with the `timingDecorator` to measure its execution time, sets a new webhook URL using the `TwilioScrapper` class from the `webscrapping.instagramWebhookChanger` module.
- **Logging the Success Message**: After setting the new webhook URL, it logs a success message to the console.

### Usage

To use this module, simply run the script. It will automatically execute the `__main__` function, which calls the `setInstagramFulfillment` function to initiate the process of setting the new webhook URL and logs a success message to the console.

### Functions

- `setNewInstagramWebhookCallbackURL(newUrl: str)`: This function sets a new webhook URL for Instagram integrations. It creates an instance of the `TwilioScrapper` class and calls its `setNewWebhookURL` and `run` methods to update the webhook URL.

- `setInstagramFulfillment()`: This function retrieves the current ngrok URL and calls the `setNewInstagramWebhookCallbackURL` function to set the new webhook URL. It also logs a success message to the console.

- `__main__()`: This function calls the `setInstagramFulfillment` function to initiate the process of setting the new webhook URL for Instagram integrations.

### Decorators

- `timingDecorator`: This decorator is used to measure the execution time of the `setNewInstagramWebhookCallbackURL` function. It is imported from the `time_decorator` module.

### External Modules

- `fulfillment.ngrokGetter`: This module contains the `get_ngrok_url` function, which is used to retrieve the current URL exposed by ngrok.
- `webscrapping.instagramWebhookChanger`: This module contains the `TwilioScrapper` class, which is used to update the webhook URL for Instagram integrations.

Ensure to have the necessary modules and dependencies installed before running the script.