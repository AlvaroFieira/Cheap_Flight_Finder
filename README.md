# Cheap Flight Finder



## Overview

The Flight Search App is a Python application designed to find and notify users about the cheapest flights available from a specified origin city. The app utilizes data from a Google Sheet for airport codes and user information and sends notifications via WhatsApp and email when low-price flights are found.

## Features

- **Airport Code Management**: Automatically updates IATA codes for cities in the Google Sheet.
- **Flight Search**: Searches for both direct and indirect flights, checking for the cheapest options.
- **Price Alert Notifications**: Sends WhatsApp and email notifications when a flight is found at a price lower than the specified threshold.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `datetime`
  - Any other libraries used in `data_manager`, `flight_search`, and `notification_manager` modules (ensure to install them).

## Setup

Configure .env file with following parameters:
1. `SHEETY_BEARER_TOKEN`
2. `AMADEUS_API_KEY`
3. `AMADEUS_API_SECRET`
4. `TWILIO_ACCOUNT_SID`
5. `TWILIO_AUTH_TOKEN`
6. `TWILIO_WHATSAPP_NUMBER`
7. `TWILIO_VERIFIED_NUMBER`
8. `SMTPLIB_FROM_EMAIL`
9. `SMTPLIB_PASSWORD`

## Configure the Application:

Set your origin airport by updating the ORIGIN_CITY_IATA variable.
Ensure that the data_manager, flight_search, and notification_manager modules are correctly implemented and configured to interact with your data sources (e.g., Google Sheets, flight APIs).
Create a Google sheet including a list of cities and the highest price the user is willing to pay to fly to these cities.

This app will:
- Update the airport codes in your Google Sheet.
- Search for the cheapest flights from the specified origin to the cities listed in the sheet.
- Send notifications if a flight is found at a lower price than specified in the sheet.

## Code Structure
- data_manager.py: Handles data retrieval and updating from Google Sheets.
- flight_search.py: Contains logic for searching flights using an API.
- notification_manager.py: Manages notifications via WhatsApp and email.
- flight_data.py: Includes functions for processing flight data, such as finding the cheapest flight.
