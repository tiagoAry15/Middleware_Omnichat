## dialogflowFulfillmentSetter.py

This module is responsible for updating the fulfillment URL in the Dialogflow project settings. It facilitates the automation of setting a new fulfillment URL, which is essential for the webhook configurations. Here are the primary functionalities of this module:

- **Loading Environment Variables**: Utilizes the `dotenv` package to load environment variables which hold the necessary credentials and project details.
- **Fetching Dialogflow Credentials**: Constructs a credentials object using the `getDialogflowCredentials` function, which gathers necessary credentials from environment variables.
- **Setting New Fulfillment URL**: The `setNewFulfillment` function is responsible for setting a new fulfillment URL in the Dialogflow project. It constructs a fulfillment object and an update mask, and then sends a request to update the fulfillment settings in Dialogflow.

### Usage

To use this module, simply run the script. It will automatically execute the `__main__` function which in turn calls the `setNewFulfillment` function to update the fulfillment URL in the Dialogflow project.

### Functions

- `getDialogflowCredentials()`: This function constructs and returns a credentials object using the information stored in environment variables. It utilizes the `service_account` module from the `google.oauth2` package to create the credentials object.

- `setNewFulfillment(newUrl: str = "https://www.facebook.com")`: This function, decorated with `timingDecorator` to measure its execution time, updates the fulfillment URL in the Dialogflow project. It constructs a fulfillment object and an update mask, and then sends a request to update the fulfillment settings in Dialogflow. The default value for the `newUrl` parameter is "https://www.facebook.com".

- `__main__()`: This function calls the `setNewFulfillment` function to initiate the process of updating the fulfillment URL in the Dialogflow project.

### Decorators

- `timingDecorator`: This decorator is used to measure the execution time of the `setNewFulfillment` function. It is imported from the `gpt.time_decorator` module.

### Environment Variables

The following environment variables are required to be set for the script to function correctly:

- `DIALOGFLOW_TYPE`
- `DIALOGFLOW_PROJECT_ID`
- `DIALOGFLOW_PRIVATE_KEY_ID`
- `DIALOGFLOW_PRIVATE_KEY`
- `DIALOGFLOW_CLIENT_EMAIL`
- `DIALOGFLOW_CLIENT_ID`
- `DIALOGFLOW_AUTH_URI`
- `DIALOGFLOW_TOKEN_URI`
- `DIALOGFLOW_AUTH_PROVIDER_X509_CERT_URL`
- `DIALOGFLOW_CLIENT_X509_CERT_URL`

Ensure that these environment variables are correctly set in your environment or in a `.env` file before running the script.
