## _fulfillmentSetter.py
This module is responsible for setting up the fulfillment URL for the chatbot. It takes the current exposed URL by ngrok 
and sets it up in to the corresponding component. It is a wrapup of several individual fulfillment's
- Dialogflow
- Instagram
- Twilio

## dialogflow_session.py
This module is responsible for setting up the session for Dialogflow. It is responsible for
- Loading the menu
- Sending the user message to dialogflow and returning the bot adequate response