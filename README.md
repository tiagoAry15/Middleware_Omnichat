# Project Overview

This project is a chatbot that allows users to order pizza through many different platforms. Actually it supports:
- Whatsapp
- Facebook
- Instagram

It is built using Dialogflow and Firebase.

![Architecture](docs/pictures/architecture.png)

# Documentation Summary

## API Configuration Component
- [API Config](docs/api_config/api_config.md)

## API Routes Component
- [Conversation Routes](docs/api_routes/conversation_routes.md)
- [Test Routes](docs/api_routes/test_routes.md)
- [User Routes](docs/api_routes/user_routes.md)

## Data Component
- [Message Converter](docs/data/message_converter.md)
- [Speisekarte Extraction](docs/data/speisekarte_extraction.md)

## Firebase Component
- [Firebase Connection](docs/firebaseFolder/firebase_connection.md)
- [Firebase Conversation](docs/firebaseFolder/firebase_conversation.md)
- [Firebase Core Wrapper](docs/firebaseFolder/firebase_core_wrapper.md)
- [Firebase Credentials](docs/firebaseFolder/firebase_credentials.md)
- [Firebase User](docs/firebaseFolder/firebase_user.md)

## Fulfillment Component
- [Dialogflow Automated Fulfillment](docs/fulfillment/dialogflowAutomatedFulfillment.md)
- [Dialogflow Fulfillment Setter](docs/fulfillment/dialogflowFulfillmentSetter.md)
- [Instagram Automated Fulfillment](docs/fulfillment/instagramAutomatedFulfillment.md)
- [Ngrok Getter](docs/fulfillment/ngrokGetter.md)

## Intent Manipulation Component
- [Dispatcher](docs/intentManipulation/dispatcher.md)
- [Intent Manager](docs/intentManipulation/intent_manager.md)

## Order Processing Component
- [Drink Processor](docs/orderProcessing/drink_processor.md)
- [Order Builder](docs/orderProcessing/order_builder.md)
- [Pizza Processor](docs/orderProcessing/pizza_processor.md)

## Socket Emissions Component
- [Socket Emissor](docs/socketEmissions/socket_emissor.md)

## Utilities Component
- [Decorators](docs/utils/decorators/)
  - [Firebase Connection Decorator](docs/utils/decorators/firebase_connection_decorator.md)
  - [Singleton Decorator](docs/utils/decorators/singleton_decorator.md)
  - [Time Decorator](docs/utils/decorators/time_decorator.md)
- [Core Utils](docs/utils/core_utils.md)
- [Env to JSON](docs/utils/env_to_json.md)
- [Helper Utils](docs/utils/helper_utils.md)
- [Instagram Utils](docs/utils/instagram_utils.md)
- [System Utils](docs/utils/system_utils.md)

# Helper Components
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

# Setup Guide

# Running the Application