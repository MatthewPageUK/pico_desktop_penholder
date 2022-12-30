#
#  Pico Desktop - Pen holder and calendar
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Gets the time from NTP and shows it on the LCD screen.
#
#  -{ Raspberry Pi Pico W }
#  -{ Pimoroni 1.3" SPI Colour Square LCD (240x240) Breakout }
#  -{ https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics }
#
#  By           - Matthew Page
#  Version      - 0.0.1
#  Date         - 30th December 2022
#
import utime
import network
import ntptime
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_P8

WIFI_SSID = "yournetwork"
WIFI_PASSWORD = "password"

display = PicoGraphics(display=DISPLAY_LCD_240X240, pen_type=PEN_P8)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()
MIDX = int(WIDTH/2)
MIDY = int(WIDTH/2)
FPS = 0.2
BG = display.create_pen(255, 255, 255)
PURPLE = display.create_pen(255, 75, 255)
GREEN = display.create_pen(32, 200, 32)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)

DEFAULT_NOTIFICATION_DELAY = 0

CALENDAR_DAYS = ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY")
CALENDAR_MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

# Day settings
DAY_FONT = "serif"
DAY_FONT_SCALE = 1
DAY_YPOS = 35
DAY_COLOUR = BLACK

# Date settings
DATE_FONT = "sans"
DATE_FONT_SCALE = 3
DATE_YPOS = 110
DATE_COLOUR = RED

# Month settings
MONTH_FONT = "serif"
MONTH_FONT_SCALE = 2.5
MONTH_YPOS = 195
MONTH_COLOUR = BLACK

# Show a notification on the display
def notification(text, colour, delay = DEFAULT_NOTIFICATION_DELAY, background = BG):
    display.set_pen(background)
    display.clear()
    display.set_pen(colour)
    display.text(text, int((WIDTH - display.measure_text(text, 2)) / 2), 110, 220, 2)
    display.update()
    utime.sleep(delay)

# Show a task / event on the display
def task(text1, text2, colour, delay = DEFAULT_NOTIFICATION_DELAY, background = BG):
    display.set_pen(background)
    display.clear()
    display.set_pen(colour)
    display.set_font('bitmap8')
    display.text(text1, 20, 20, 200, 4)
    display.set_font('bitmap8')
    display.text(text2, 20, 60, 200, 3)
    
    display.update()
    utime.sleep(delay)

# Connect to WiFi and get time
def setNtpTime(ssid, password):
    notification("Setting time...", GREEN)

    wifiNetwork = network.WLAN(network.STA_IF)
    wifiNetwork.active(True)
    wifiNetwork.connect(ssid, password)

    notification("Connecting to WIFI...", GREEN)
    wifiCount = 1
    while wifiNetwork.status() != network.STAT_GOT_IP:
        notification("Connecting... {c}".format(c=wifiCount), GREEN, 1)
        wifiCount += 1

    notification("Getting NTP time", GREEN)
    ntptime.settime()

    wifiNetwork.disconnect()
    wifiNetwork.active(False)
    notification("Done", PURPLE)

    return True

notification("Starting up...", PURPLE, 2)

# Get the time
setNtpTime(WIFI_SSID, WIFI_PASSWORD)

# Main Loop
while True:
    
    task('8:30am', 'Take the dog for a walk', GREEN, 5)
    task('10:30am', 'Important business meeting with Bob and Alice, don\'t tell Charlie', PURPLE, 5)

    # The date now
    date = utime.localtime()
    
    # Get the day and month
    weekdayNumber = date[6]
    day = date[2]
    month = date[1]

    # Get the day and month names
    dayName = CALENDAR_DAYS[weekdayNumber]
    monthName = CALENDAR_MONTHS[month - 1]

    # Clear the screen
    display.set_pen(BG)
    display.clear()

    # Draw the day name
    display.set_font(DAY_FONT)
    display.set_pen(DAY_COLOUR)
    xpos = int((WIDTH - display.measure_text(dayName, DAY_FONT_SCALE)) / 2)
    display.text(dayName, xpos, DAY_YPOS, 0, DAY_FONT_SCALE)
    
    # Draw the date
    display.set_font(DATE_FONT)
    display.set_pen(DATE_COLOUR)
    text = str(day)
    twidth = display.measure_text(text, DATE_FONT_SCALE)
    xpos = int((WIDTH - twidth) / 2)
    display.text(text, xpos, DATE_YPOS, 0, DATE_FONT_SCALE)
    # Repeat it at 1 pixel offset to make somewhat bolder
    display.text(text, xpos + 1, DATE_YPOS, 0, DATE_FONT_SCALE)
    display.text(text, xpos - 1, DATE_YPOS, 0, DATE_FONT_SCALE)
    display.text(text, xpos - 1, DATE_YPOS - 1, 0, DATE_FONT_SCALE)
    display.text(text, xpos + 1, DATE_YPOS - 1, 0, DATE_FONT_SCALE)
    display.text(text, xpos + 1, DATE_YPOS + 1, 0, DATE_FONT_SCALE)
    display.text(text, xpos - 1, DATE_YPOS + 1, 0, DATE_FONT_SCALE)  
    
    # Draw the month name
    display.set_font(MONTH_FONT)
    display.set_pen(MONTH_COLOUR)
    xpos = int((WIDTH - display.measure_text(monthName, MONTH_FONT_SCALE)) / 2)
    display.text(monthName, xpos, MONTH_YPOS, 0, MONTH_FONT_SCALE)
    
    # Update the display
    display.update()

    # Sleep a while - we could sleep until tomorrow
    utime.sleep(1 / FPS)