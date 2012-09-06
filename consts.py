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
# You can customize your Infoscreen by changing the constants in this file.
# 

# Constants for all time strings. You can theoretically change the language by
# changing these, but you might also need to update the code if your language
# doesn't follow the same pattern as English.
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

# Screen size, and whether it should be full screen or not.
# FULLSCREEN is usually  False for testing; True for live.

WIDTH = 1024
HEIGHT = 768
FULLSCREEN = False

# Messages - the filename to load them from, and how long to display each one.

MESSAGES_FNAME = 'messages.txt'
TICKS_PER_MESSAGE = 50

# Position and size of the clock.

CENTER_X = WIDTH/2		# center of clock
CENTER_Y = HEIGHT/2
RADIUS = 285			# radius of main circle
RADIUS_OUTER = RADIUS+20	# radius of marker circle
DOT_SIZE = 15			# diameter of a dot

HOUR_RADIUS = RADIUS * 0.5	# radius of the hands
MINS_RADIUS = RADIUS * 0.9

HANDS_COLOR = (0, 255, 255)	# colour of the hands; (0 0 0) for invisible

DIGIT_SPACING = 100		# spacing between the digital clock digits
SMALL_DIGIT_SPACING = 80

# Position of the text. Offsets from the size of the screen for the various
# relevant positions.

TEXT_LEFT_OFFSET=10
TEXT_RIGHT_OFFSET=10
TEXT_TOP_OFFSET=1
TEXT_BOTTOM_OFFSET=70

# The font that we're going to use. None selects a default font.

TEXT_FONT=None
TEXT_SIZE=52

