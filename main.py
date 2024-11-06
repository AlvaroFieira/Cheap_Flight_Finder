import data_manager as dm
import flight_search as fs
import notification_manager as nm
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
import time

# ==================== Set up the Flight Search ====================

data_manager = dm.DataManager()
flight_search = fs.FlightSearch()
notification_manager = nm.NotificationManager()

cities = data_manager.get_rows_from_prices()
users = data_manager.get_rows_from_users()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================
for city in cities:
    if city['iataCode'] == '':
        IATACode = flight_search.obtain_iata_code(city['city'])
        city['iataCode'] = IATACode
        data_manager.update_row_from_prices(row_id=city['id'], field='iataCode', value=IATACode)

# ==================== Search for Flights ====================

in_30_days = datetime.now() + timedelta(days=30)
in_45_days = datetime.now() + timedelta(days=45)

for destination in cities:

    print(f"Getting flights for {destination['city']}...")

    # ==================== Search for direct flights  ====================

    flights = flight_search.find_cheap_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=in_30_days,
        to_time=in_45_days
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

    # ==================== Search for indirect flight if N/A ====================

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.find_cheap_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=in_30_days,
            to_time=in_45_days,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:

        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        notification_manager.send_whatsapp(message_body=message)

        for user in users:
            notification_manager.send_email(
                to_addrs=user['whatIsYourEmailAddress?'],
                message_body=message
            )
