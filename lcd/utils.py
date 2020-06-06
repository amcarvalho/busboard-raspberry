from RPLCD.i2c import CharLCD

LCD_ROWS = 4
LCD_COLUMNS = 20
MAX_DESTINATION_LENGTH = 10
LINE_FORMAT = "{0:<1} {1:>3} {2:<10} {3:>3}"


def get_board_bus_line(order, route, destination, due_in, iteration=0) -> str:
    if len(destination) <= MAX_DESTINATION_LENGTH:
        truncated_destination = destination
    else:
        i = (iteration % (len(destination) - MAX_DESTINATION_LENGTH + 1))
        truncated_destination = destination[i: MAX_DESTINATION_LENGTH + i]
    return LINE_FORMAT.format(order, route, truncated_destination, due_in)


def get_board_bus(buses, iteration=0):
    lines = [get_board_bus_line(buses[i][0], buses[i][1], buses[i][2], buses[i][3], iteration) for i in range(len(buses))]
    for i in range((LCD_ROWS - len(lines))):
        lines.append("--------------------")
    return "\r\n".join(lines)


class LcdUtils:
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x27,
            port=1,
            cols=LCD_COLUMNS,
            rows=LCD_ROWS,
            dotsize=8,
            charmap='A02',
            auto_linebreaks=True,
            backlight_enabled=True
        )

