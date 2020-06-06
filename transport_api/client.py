import json
import logging
import os
import requests
import time
from datetime import datetime
from lcd import utils

log = logging.getLogger(__name__)


class TransportApiClient:
    def __init__(self):
        self.app_id = os.getenv("TRANSPORT_API_APP_ID")
        self.app_key = os.getenv("TRANSPORT_API_APP_KEY")
        self.bus_stop = os.getenv("TRANSPORT_API_BUS_STOP")
        self.hours_without_updates = os.getenv(
            "TRANSPORT_API_HOURS_WITHOUT_UPDATES", "20,21,22,23,00,01,02,03,04,05,06,07"
        )
        self.group_results_by_route = "no"
        self.next_buses = "yes"
        self.limit_results = utils.LCD_ROWS

    def get_bus_departures(self):
        output = []
        if time.strftime("%H") in self.hours_without_updates.split(","):
            log.warning("Not fetching results. Current time falls within the excluded hours. To change this behaviour "
                        "define environment variable TRANSPORT_API_HOURS_WITHOUT_UPDATES=23,00,01,etc")
            return output

        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'group': self.group_results_by_route,
            'limit': self.limit_results,
            'nextbuses': self.next_buses
        }
        url = f"https://transportapi.com/v3/uk/bus/stop/{self.bus_stop}/live.json"
        response = requests.get(url, params=params)
        response_data = json.loads(response.text)
        departures = response_data['departures']['all']
        i = 1
        for departure in departures:
            output_item = [i, departure['line'], departure['direction']]
            departure_time = datetime.strptime(
                f"{departure['expected_departure_date']} {departure['expected_departure_time']}",
                "%Y-%m-%d %H:%M"
            )
            due_in = divmod((departure_time - datetime.now()).total_seconds(), 60)[0]
            if due_in <= 0:
                output_item.append("due")
            else:
                output_item.append(str(int(due_in)) + "m")
            output.append(output_item)
            i += 1
        return output
