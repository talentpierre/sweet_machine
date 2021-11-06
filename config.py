'''Config File'''

import sys

#the kind of display available and used
display = "waveshare2in13"

#opennode credentials
read_only_key = ""

######################################################
### (Do not change and of these parameters unless  ###
### you know exactly what you are doing.           ###
######################################################

WHITE = 1
BLACK = 0
# Display - Waveshare 2.13 is 250 * 122 pixels
if display == "waveshare2in13":
    try:
        from waveshare_epd import epd2in13_V2
        WAVESHARE = epd2in13_V2.EPD()
    except ImportError:
        sys.exit("Exiting...")

# Display - Waveshare 2.13 (D) is 212 * 104 pixels
elif display == "waveshare2in13d":
    try:
        from waveshare_epd import epd2in13d
        WAVESHARE = epd2in13d.EPD()
    except ImportError:
        sys.exit("Exiting...")

# Display - No configuration match
else:
    sys.exit("Exiting...")

# Button
LASTPUSHES = 0
PUSHES = 0
