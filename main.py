from lcd import utils as lcd_utils
from transport_api import client as transport_api_client
import time

if __name__ == "__main__":
    tac = transport_api_client.TransportApiClient()
    lu = lcd_utils.LcdUtils()
    while True:
        buses = tac.get_bus_departures()
        for i in range(105):
            lu.lcd.write_string(lcd_utils.get_board_bus(buses, i))
            time.sleep(0.3)