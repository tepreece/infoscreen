# Copyright (c) 2009 - 2012 Thomas Preece
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# 
# Don't change these constants
# 

LEFT = 0
RIGHT = 1
CENTER = 2

# 
# You can customize your Infoscreen by changing the rest of this file.
# 

# 
# General settings
# 

# Basic window parameters
# For best results, set WIDTH and HEIGHT to the native resolution of the monitor
# you intend to use for displaying the Infoscreen. You might want to leave
# FULLSCREEN turned off for testing; set it to True when you are ready to
# deploy your configuration to the live environment.
WIDTH = 1024
HEIGHT = 768
FULLSCREEN = False

# Find the center of the screen - we'll be using this later to line things up.
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

# Where are the image files stored? Usually best to set an absolute path if
# possible - it's set to a relative path by default so it should work out of
# the box.
IMAGE_DIR = './images'

# Where to get information from (json)
INFO_FNAME = 'info.json'

# font to be used by digital clock and backtimer
CLOCK_FONT = 'clock.ttf'

# 
# Digital Clock
# By default this displays the current time as HH:MM in large red digits.
# 

SHOW_DIGITAL = True					# Should we render the digital clock?
DIGITAL_SECONDS = False				# False - HH:MM; True - HH:MM:SS
DIGITAL_FONT_SIZE = 200
DIGITAL_X = CENTER_X
DIGITAL_Y = CENTER_Y - 150


# 
# Backtimer
# This displays MM:SS until the top of the next hour. 

SHOW_BACKTIMER = True				# Should we render the backtimer?
BACKTIMER_FONT_SIZE = 150
BACKTIMER_MINUS = True				# Should we show a minus at the start?
BACKTIMER_X = CENTER_X		
BACKTIMER_Y = CENTER_Y			

# 
# Dots
# This represents the seconds of the current minute as a ring of dots. You can
# also display marker dots at five-second intervals, that appear outside the
# main ring. To customize the appearance, change "dot.png".
# 

SHOW_DOTS = True						# Should we render the ring of dots?
SHOW_MARKER_DOTS = False					# Should we render the marker dots?
DOTS_CENTER_X = CENTER_X				# Where should the center of the dots circle(s) be?
DOTS_CENTER_Y = CENTER_Y
DOTS_RADIUS = 285						# Radius of the main circle
MARKER_DOTS_RADIUS = DOTS_RADIUS  +20	# Radius of the marker circle
DOT_SIZE = 15							# The diameter of a dot

# 
# Analog Clock
# You can render the following elements: hour hand, minute hand, second hand,
# hub, ring. Whenever you show an analog clock, you should always show a hub,
# as this covers up imperfections in the rendering at the centre of the clock.
# To display a coloured background, set the ring thickness to 0. This will
# render a filled circle. Obviously you should set ring colour different to
# hands colour in this case!
# 

SHOW_ANALOG = False				# Should we render the analog clock?
SHOW_RING = False				# Should we render the ring / background circle?
ANALOG_CENTER_X = CENTER_X		# Where should the center of the clock be?
ANALOG_CENTER_Y = CENTER_Y
HOUR_RADIUS = DOTS_RADIUS * 0.5	# What should the lengths of the hands be?
MINS_RADIUS = DOTS_RADIUS * 0.9	# You can define this in terms of DOTS_RADIUS, or as a simple number.
SECS_RADIUS = 0					# Set a hand length to zero to hide it.
HUB_RADIUS = 10					# Radius of the hub
RING_RADIUS = 90				# Radius of the ring / background circle.
HOUR_THICKNESS = 8				# Thicknesses of the hands
MINS_THICKNESS = 4
SECS_THICKNESS = 2
RING_THICKNESS = 1
HOUR_COLOR = (0, 255, 255)		# Colors for the various elements
MINS_COLOR = (0, 255, 255)
SECS_COLOR = (0, 255, 255)
HUB_COLOR = (0, 255, 255)
RING_COLOR = (0, 255, 255)

# 
# Human-Readable Time Text
# This shows the current time as a string that the presenters can read out
# directly. You can translate this by changing the strings for the various
# numbers - note that this will only work if your language is a similar
# structure to English.
# 

SHOW_TIME_TEXT = True				# Should we render the time text?
LOWERCASE_HOURS = True				# Should we force the hour part to lower case?
TIME_TEXT_X = 10					# Where should we render the time text?
TIME_TEXT_Y = 1						# This must be the top of the text.
TIME_TEXT_ALIGN = LEFT				# Left, right or center align from the origin?
TIME_TEXT_FONT = None				# Specify the font to be used. If None, use default.
TIME_TEXT_SIZE = 52

MINUTES = (
	'',
	'One minute',
	'Two minutes',
	'Three minutes',
	'Four minutes',
	'Five',
	'Six minutes',
	'Seven minutes',
	'Eight minutes',
	'Nine minutes',
	'Ten',
	'Eleven minutes',
	'Twelve minutes',
	'Thirteen minutes',
	'Fourteen minutes',
	'Quarter',
	'Sixteen minutes',
	'Seventeen minutes',
	'Eighteen minutes',
	'Nineteen minutes',
	'Twenty',
	'Twenty-one minutes',
	'Twenty-two minutes',
	'Twenty-three minutes',
	'Twenty-four minutes',
	'Twenty-five',
	'Twenty-six minutes',
	'Twenty-seven minutes',
	'Twenty-eight minutes',
	'Twenty-nine minutes',
	'Half',
)

HOURS = (
	'Midnight',
	'One',
	'Two',
	'Three',
	'Four',
	'Five',
	'Six',
	'Seven',
	'Eight',
	'Nine',
	'Ten',
	'Eleven',
	'Twelve',
	'One',
	'Two',
	'Three',
	'Four',
	'Five',
	'Six',
	'Seven',
	'Eight',
	'Nine',
	'Ten',
	'Eleven',
	'Midnight',
)

PAST = 'past'
TO = 'to'
OCLOCK = 'o\'clock'

# 
# Human-Readable Date Text
# 

SHOW_DATE_TEXT = True				# Should we render the date text?
DATE_TEXT_FORMAT = '%A %d %B'		# See: http://docs.python.org/library/time.html#time.strftime
DATE_TEXT_X = WIDTH-10
DATE_TEXT_Y = 1
DATE_TEXT_ALIGN = RIGHT
DATE_TEXT_FONT = None
DATE_TEXT_SIZE = 52

# 
# Messages
# These are stored in the file specified. To re-read the messages at run time,
# send a SIGHUP to the program. The message file format is:
# red green blue Message text
# eg: 255 0 255 This is a message in fuchsia.
# 

SHOW_MESSAGES = False				# Should we render the messages?
MESSAGES_FNAME = 'messages.txt'		# What file should we read the messages from? Absolute path is best.
TICKS_PER_MESSAGE = 50				# 1 tick is approximately 1/10 s
MESSAGE_X = 10				# Color, position, align and font as for time and date - see above. 
MESSAGE_Y = HEIGHT-55
MESSAGE_ALIGN = LEFT
MESSAGE_TEXT_FONT = None
MESSAGE_TEXT_SIZE = 52

#
# Trackinfo

SHOW_TRACKINFO = True
SHOW_PROGRESS = True
PROGRESS_BAR_HEIGHT= 64
SHOW_REMAINING = True

NP_FONT = None
NP_FONT_SIZE = 52
REMAINS_FONT = None
REMAINS_FONT_SIZE = 36

SHOW_ONAIR = True
ONAIR_Y = HEIGHT - 80
ONAIR_FONT = None
ONAIR_FONT_SIZE = 36

# Colors

COLOR = {
		'DIGITAL': (255, 0, 0),
		'BACKTIMER': (0, 255, 0),
		'SHOW': (41, 255, 211),
		'ONAIR': (150, 255, 211),
		'TRACK_INFO': (255, 255, 255),
		'TRACK_REMAINS': (200, 200, 200),
		'PROGRESS_FG': (100, 0, 255),
		'PROGRESS_BG': (30, 0, 100),
		'TIME': (255, 255, 255),
		'DATE': (255, 255, 255)
		}

# 
# END
#

# Process management. We store the process ID of the process in a PID file. This
# allows us to tell if Infoscreen is already running, and allows other processes
# to send signals to the right place. We can also (optionally) delete the PID
# file when Infoscreen terminates, and only allow one Infoscreen to run at any
# one time.

USE_PIDFILE = False				# Set to False to bypass all PID file code
								# (probably required to run on Windows)
PIDFILE = 'infoscreen.pid'		# What is the name of our PID file?
DELETE_PIDFILE_ON_EXIT = True	# Potentially unsafe if we allow multiple instances
ALLOW_MULTIPLE_INSTANCES = False

