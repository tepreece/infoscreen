#!/usr/bin/env python

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

import sys
import os
import signal
import time
import math

import pygame
from pygame.locals import *

from consts import *

# constants
NORMAL = 0
DEADAIR = 1

COLON = 10
MINUS = 11

# globals
mode = NORMAL

messages = [
	'Infoscreen (c) Thomas Preece 2009-12'
]

messagecolors = [
	(0, 255, 0)
]

currentmessage = 0
messagesreloaded = False

# signal handlers
def sigusr1(signum, frame):
	# SIGUSR1 - enable dead air mode
	global mode
	mode = DEADAIR

def sigusr2(signum, frame):
	# SIGUSR2 - disable dead air mode
	global mode
	mode = NORMAL

def sighup(signum, frame):
	# SIGHUP - reload configuration
	reload_messages()

def reload_messages():
	global messages, messagecolors, currentmessage, messagesreloaded

	f = open(MESSAGES_FNAME, 'r')
	
	messages = []
	messagecolors = []

	for line in f:
		items = line.strip().split(None, 3)
		messages.append(items[3])
		color = (int(items[0]), int(items[1]), int(items[2]))
		if color==(0, 0, 0): color = (255, 255, 255)
		messagecolors.append(color)
		
	currentmessage = 0
	messagesreloaded = True
	f.close()

reload_messages()

# start pygame

pygame.init()
if FULLSCREEN:
	window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
	window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Infoscreen')
pygame.mouse.set_visible(False)
screen = pygame.display.get_surface()

timefont = pygame.font.Font(TEXT_FONT, TEXT_SIZE)

# load surfaces

nums = [
	pygame.image.load('images/7seg0.png'),
	pygame.image.load('images/7seg1.png'),
	pygame.image.load('images/7seg2.png'),
	pygame.image.load('images/7seg3.png'),
	pygame.image.load('images/7seg4.png'),
	pygame.image.load('images/7seg5.png'),
	pygame.image.load('images/7seg6.png'),
	pygame.image.load('images/7seg7.png'),
	pygame.image.load('images/7seg8.png'),
	pygame.image.load('images/7seg9.png'),
	pygame.image.load('images/7segc.png'),
]

nums_small = [
	pygame.image.load('images/small_7seg0.png'),
	pygame.image.load('images/small_7seg1.png'),
	pygame.image.load('images/small_7seg2.png'),
	pygame.image.load('images/small_7seg3.png'),
	pygame.image.load('images/small_7seg4.png'),
	pygame.image.load('images/small_7seg5.png'),
	pygame.image.load('images/small_7seg6.png'),
	pygame.image.load('images/small_7seg7.png'),
	pygame.image.load('images/small_7seg8.png'),
	pygame.image.load('images/small_7seg9.png'),
	pygame.image.load('images/small_7segc.png'),
	pygame.image.load('images/small_7segm.png'),
]

dot_red = pygame.image.load('images/dot-red.png')

for num in nums:
	num.set_colorkey((0, 0, 0))
for num in nums_small:
	num.set_colorkey((255, 0, 255))
dot_red.set_colorkey((0, 0, 0))

surf_deadair = pygame.image.load('images/deadair.png')

# set up signal handlers
signal.signal(signal.SIGUSR1, sigusr1)
signal.signal(signal.SIGUSR2, sigusr2)
signal.signal(signal.SIGHUP, sighup)

currentmessage = 0
count = 0

# calculate dot positions
DOTS_X = []
DOTS_Y = []
OUTER_DOTS_X = []
OUTER_DOTS_Y = []

for i in xrange(60):
	deg = 6*i - 90
	rad = math.radians(deg)
	
	DOTS_X.append(CENTER_X + RADIUS * math.cos(rad) - DOT_SIZE/2)
	DOTS_Y.append(CENTER_Y + RADIUS * math.sin(rad) - DOT_SIZE/2)
	
	if (i % 5)==0:
		OUTER_DOTS_X.append(CENTER_X + RADIUS_OUTER * math.cos(rad) - DOT_SIZE/2)
		OUTER_DOTS_Y.append(CENTER_Y + RADIUS_OUTER * math.sin(rad) - DOT_SIZE/2)

while True:	
	# do drawing
	if mode == DEADAIR:
		screen.blit(surf_deadair, (0, 0))
	else:
		screen.fill((0, 0, 0))
		
		# draw reference dots
		for i in xrange(12):
			screen.blit(dot_red, (OUTER_DOTS_X[i], OUTER_DOTS_Y[i]))
		
		# get time data
		timedata = time.localtime()
		hour = timedata[3]
		mins = timedata[4]
		secs = timedata[5]
		
		# draw dots
		for i in xrange(secs+1):
			screen.blit(dot_red, (DOTS_X[i], DOTS_Y[i]))
		
		# draw hour hand
		deg = ((hour % 12) * 30) + (mins / 2) - 90
		rad = math.radians(deg)
		
		x = CENTER_X + (math.cos(rad) * HOUR_RADIUS)
		y = CENTER_Y + (math.sin(rad) * HOUR_RADIUS)
		
		pygame.draw.line(screen, HANDS_COLOR, (CENTER_X, CENTER_Y), (x, y), 8)
		
		# draw minute hand
		deg = (mins * 6) + (secs / 10) - 90
		#deg = (mins * 60) + (secs / 2) - 90
		rad = math.radians(deg)
		
		x = CENTER_X + (math.cos(rad) * MINS_RADIUS)
		y = CENTER_Y + (math.sin(rad) * MINS_RADIUS)
		
		pygame.draw.line(screen, HANDS_COLOR, (CENTER_X, CENTER_Y), (x, y), 4)
		
		# draw hub
		pygame.draw.circle(screen, HANDS_COLOR, (CENTER_X, CENTER_Y), 10)
		
		# draw large numbers
		digit1 = int(hour / 10)
		digit2 = hour % 10
		digit3 = int(mins / 10)
		digit4 = mins % 10
		
		x = CENTER_X - 215
		y = CENTER_Y - 156
		
		screen.blit(nums[digit1], (x, y))
		x += DIGIT_SPACING
		screen.blit(nums[digit2], (x, y))
		x += DIGIT_SPACING
		screen.blit(nums[COLON], (x, y))
		x += 29
		screen.blit(nums[digit3], (x, y))
		x += DIGIT_SPACING
		screen.blit(nums[digit4], (x, y))
		
		# draw small numbers
		minsleft = 59 - mins
		secsleft = 60 - secs
		if secsleft==60:
			secsleft = 0
			minsleft += 1
		if minsleft==60:
			minsleft = 0
		
		digit1 = int(minsleft / 10)
		digit2 = minsleft % 10
		digit3 = int(secsleft / 10)
		digit4 = secsleft % 10
		
		x = CENTER_X - 215
		y = CENTER_Y + 12
		
		screen.blit(nums_small[MINUS], (x, y))
		x += SMALL_DIGIT_SPACING
		screen.blit(nums_small[digit1], (x, y))
		x += SMALL_DIGIT_SPACING
		screen.blit(nums_small[digit2], (x, y))
		x += SMALL_DIGIT_SPACING
		screen.blit(nums_small[COLON], (x, y))
		x += 29
		screen.blit(nums_small[digit3], (x, y))
		x += SMALL_DIGIT_SPACING
		screen.blit(nums_small[digit4], (x, y))
		
		# draw time text
		pastto = ' '+PAST+' '
		if mins > 30:
			mins = 60 - mins
			hour += 1
			pastto = ' '+TO+' '
		
		timestr = ''
		if mins == 0:
			if hour == 0 or hour == 24:
				timestr = HOURS[hour]
			else:
				timestr = HOURS[hour] + ' '+OCLOCK
		else:
			timestr = MINUTES[mins] + pastto + HOURS[hour]
		
		text = timefont.render(timestr, True, (255, 255, 255))
		screen.blit(text, (TEXT_LEFT_OFFSET, TEXT_TOP_OFFSET))
		
		# draw date text
		datestr = time.strftime('%A %d %B')
		text = timefont.render(datestr, True, (255, 255, 255))
		screen.blit(text, (WIDTH-text.get_width()-TEXT_RIGHT_OFFSET, TEXT_TOP_OFFSET))
		
		# draw message text
		if messagesreloaded:
			messagesreloaded = False
			count = 0
		count += 1
		if count == TICKS_PER_MESSAGE:
			count = 0
			currentmessage += 1
			if currentmessage == len(messages):
				currentmessage = 0
		text = timefont.render(messages[currentmessage], True, messagecolors[currentmessage])
		screen.blit(text, (TEXT_LEFT_OFFSET, HEIGHT-TEXT_BOTTOM_OFFSET))
	
	pygame.display.flip()
	
	# process events
	events = pygame.event.get()
	for event in events:
		if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
			sys.exit(0)
	
	# delay
	time.sleep(0.1)





