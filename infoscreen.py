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

from config import *

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
	if SHOW_MESSAGES:
		reload_messages()

def reload_messages():
	global messages, messagecolors, currentmessage

	f = open(MESSAGES_FNAME, 'r')
	
	messages = []
	messagecolors = []

	for line in f:
		try:
			items = line.strip().split(None, 3)
			messages.append(items[3])
			color = (int(items[0]), int(items[1]), int(items[2]))
			if color==(0, 0, 0): color = (255, 255, 255)
			messagecolors.append(color)
		except:
			print "ERROR - can't process message line: "+line
	
	if currentmessage >= len(messages):
		currentmessage = 0
	f.close()

reload_messages()

def render_text(screen, font, text, x, y, color, align=LEFT):
	surf = font.render(text, True, color)
	if align == RIGHT:
		x -= surf.get_width()
	elif align == CENTER:
		x -= (surf.get_width()/2)
	
	screen.blit(surf, (x, y))

# main code starts here

if USE_PIDFILE:
	# check to see whether the PID file already exists
	if os.access(PIDFILE, os.F_OK):
		# PID file exists - check to see whether the process is still running
		pf = open(PIDFILE, 'r')
		old_pid = pf.readline()
		if os.path.exists("/proc/%s" % old_pid):
			# Infoscreen is already running
			if not ALLOW_MULTIPLE_INSTANCES:
				print 'Infoscreen is already running as PID %s' % old_pid
				sys.exit(1)
		else:
			# redundant PID file - get rid of it
			os.remove(PIDFILE)

	# write the PID file
	pid = str(os.getpid())
	f = open(PIDFILE, 'w')
	f.write(pid)
	f.close()

# start pygame

pygame.init()
if FULLSCREEN:
	window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
	window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Infoscreen')
pygame.mouse.set_visible(False)
screen = pygame.display.get_surface()

# load fonts
timefont = pygame.font.Font(TIME_TEXT_FONT, TIME_TEXT_SIZE)
datefont = pygame.font.Font(DATE_TEXT_FONT, DATE_TEXT_SIZE)
messagefont = pygame.font.Font(MESSAGE_TEXT_FONT, MESSAGE_TEXT_SIZE)

# load surfaces

digital_nums = [
	pygame.image.load(IMAGE_DIR+'/digital0.png'),
	pygame.image.load(IMAGE_DIR+'/digital1.png'),
	pygame.image.load(IMAGE_DIR+'/digital2.png'),
	pygame.image.load(IMAGE_DIR+'/digital3.png'),
	pygame.image.load(IMAGE_DIR+'/digital4.png'),
	pygame.image.load(IMAGE_DIR+'/digital5.png'),
	pygame.image.load(IMAGE_DIR+'/digital6.png'),
	pygame.image.load(IMAGE_DIR+'/digital7.png'),
	pygame.image.load(IMAGE_DIR+'/digital8.png'),
	pygame.image.load(IMAGE_DIR+'/digital9.png'),
	pygame.image.load(IMAGE_DIR+'/digitalc.png'),
]

backtimer_nums = [
	pygame.image.load(IMAGE_DIR+'/backtimer0.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer1.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer2.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer3.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer4.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer5.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer6.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer7.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer8.png'),
	pygame.image.load(IMAGE_DIR+'/backtimer9.png'),
	pygame.image.load(IMAGE_DIR+'/backtimerc.png'),
	pygame.image.load(IMAGE_DIR+'/backtimerm.png'),
]

dot_red = pygame.image.load(IMAGE_DIR+'/dot.png')

for num in digital_nums:
	num.set_colorkey((0, 0, 0))
for num in backtimer_nums:
	num.set_colorkey((255, 0, 255))
dot_red.set_colorkey((0, 0, 0))

surf_deadair = pygame.image.load(IMAGE_DIR+'/deadair.png')

# set up signal handlers
signal.signal(signal.SIGUSR1, sigusr1)
signal.signal(signal.SIGUSR2, sigusr2)
signal.signal(signal.SIGHUP, sighup)

currentmessage = 0
count = 0

# calculate dot positions
DOTS_X = []
DOTS_Y = []
MARKER_DOTS_X = []
MARKER_DOTS_Y = []

for i in xrange(60):
	deg = 6*i - 90
	rad = math.radians(deg)
	
	DOTS_X.append(DOTS_CENTER_X + DOTS_RADIUS * math.cos(rad) - DOT_SIZE/2)
	DOTS_Y.append(DOTS_CENTER_Y + DOTS_RADIUS * math.sin(rad) - DOT_SIZE/2)
	
	if (i % 5)==0:
		MARKER_DOTS_X.append(DOTS_CENTER_X + MARKER_DOTS_RADIUS * math.cos(rad) - DOT_SIZE/2)
		MARKER_DOTS_Y.append(DOTS_CENTER_Y + MARKER_DOTS_RADIUS * math.sin(rad) - DOT_SIZE/2)

done = False
while not done:	
	# do drawing
	screen.fill((0, 0, 0))
	
	# get time data
	timedata = time.localtime()
	hour = timedata[3]
	mins = timedata[4]
	secs = timedata[5]
	
	# draw dots
	if SHOW_DOTS:
		for i in xrange(secs+1):
			screen.blit(dot_red, (DOTS_X[i], DOTS_Y[i]))
	
	# draw marker dots
	if SHOW_MARKER_DOTS:
		for i in xrange(12):
			screen.blit(dot_red, (MARKER_DOTS_X[i], MARKER_DOTS_Y[i]))
	
	# draw analog clock
	if SHOW_ANALOG:
		# draw ring
		if SHOW_RING:
			pygame.draw.circle(screen, ANALOG_RING_COLOR, (ANALOG_CENTER_X, ANALOG_CENTER_Y), RING_RADIUS, RING_THICKNESS)
		
		# draw hour hand
		deg = ((hour % 12) * 30) + (mins / 2) - 90
		rad = math.radians(deg)
	
		x = ANALOG_CENTER_X + (math.cos(rad) * HOUR_RADIUS)
		y = ANALOG_CENTER_Y + (math.sin(rad) * HOUR_RADIUS)
	
		pygame.draw.line(screen, HOUR_COLOR, (ANALOG_CENTER_X, ANALOG_CENTER_Y), (x, y), HOUR_THICKNESS)
	
		# draw minute hand
		deg = (mins * 6) + (secs / 10) - 90
		rad = math.radians(deg)
	
		x = ANALOG_CENTER_X + (math.cos(rad) * MINS_RADIUS)
		y = ANALOG_CENTER_Y + (math.sin(rad) * MINS_RADIUS)
	
		pygame.draw.line(screen, MINS_COLOR, (ANALOG_CENTER_X, ANALOG_CENTER_Y), (x, y), MINS_THICKNESS)
		
		# draw second hand
		deg = (secs * 6) - 90
		rad = math.radians(deg)
	
		x = ANALOG_CENTER_X + (math.cos(rad) * SECS_RADIUS)
		y = ANALOG_CENTER_Y + (math.sin(rad) * SECS_RADIUS)
	
		pygame.draw.line(screen, SECS_COLOR, (ANALOG_CENTER_X, ANALOG_CENTER_Y), (x, y), SECS_THICKNESS)
	
		# draw hub
		pygame.draw.circle(screen, HUB_COLOR, (ANALOG_CENTER_X, ANALOG_CENTER_Y), HUB_RADIUS)
		
	
	# draw digital clock
	if SHOW_DIGITAL:
		(digit1, digit2) = divmod(hour, 10)
		(digit3, digit4) = divmod(mins, 10)
		(digit5, digit6) = divmod(secs, 10)
		
		x = DIGITAL_X
		y = DIGITAL_Y
		
		screen.blit(digital_nums[digit1], (x, y))
		x += DIGITAL_DIGIT_SPACING
		screen.blit(digital_nums[digit2], (x, y))
		x += DIGITAL_DIGIT_SPACING
		screen.blit(digital_nums[COLON], (x, y))
		x += DIGITAL_SEPARATOR_SPACING
		screen.blit(digital_nums[digit3], (x, y))
		x += DIGITAL_DIGIT_SPACING
		screen.blit(digital_nums[digit4], (x, y))
		
		if DIGITAL_SECONDS:
			x += DIGITAL_DIGIT_SPACING
			screen.blit(digital_nums[COLON], (x, y))
			x += DIGITAL_SEPARATOR_SPACING
			screen.blit(digital_nums[digit5], (x, y))
			x += DIGITAL_DIGIT_SPACING
			screen.blit(digital_nums[digit6], (x, y))
	
	# draw backtimer
	if SHOW_BACKTIMER:
		minsleft = 59 - mins
		secsleft = 60 - secs
		if secsleft==60:
			secsleft = 0
			minsleft += 1
		if minsleft==60:
			minsleft = 0
	
		(digit1, digit2) = divmod(minsleft, 10)
		(digit3, digit4) = divmod(secsleft, 10)
	
		x = BACKTIMER_X
		y = BACKTIMER_Y
		
		if BACKTIMER_MINUS:
			screen.blit(backtimer_nums[MINUS], (x, y))
			x += BACKTIMER_MINUS_SPACING
		
		screen.blit(backtimer_nums[digit1], (x, y))
		x += BACKTIMER_DIGIT_SPACING
		screen.blit(backtimer_nums[digit2], (x, y))
		x += BACKTIMER_DIGIT_SPACING
		screen.blit(backtimer_nums[COLON], (x, y))
		x += BACKTIMER_SEPARATOR_SPACING
		screen.blit(backtimer_nums[digit3], (x, y))
		x += BACKTIMER_DIGIT_SPACING
		screen.blit(backtimer_nums[digit4], (x, y))
	
	# draw time text
	if SHOW_TIME_TEXT:
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
			if LOWERCASE_HOURS:
				timestr = MINUTES[mins] + pastto + HOURS[hour].lower()
			else:
				timestr = MINUTES[mins] + pastto + HOURS[hour]
		
		render_text(screen, timefont, timestr, TIME_TEXT_X, TIME_TEXT_Y, TIME_TEXT_COLOR, TIME_TEXT_ALIGN)
	
	# draw date text
	if SHOW_DATE_TEXT:
		datestr = time.strftime(DATE_TEXT_FORMAT)
		render_text(screen, datefont, datestr, DATE_TEXT_X, DATE_TEXT_Y, DATE_TEXT_COLOR, DATE_TEXT_ALIGN)
	
	# draw message text
	if SHOW_MESSAGES:
		count += 1
		if count == TICKS_PER_MESSAGE:
			count = 0
			currentmessage += 1
			if currentmessage >= len(messages):
				currentmessage = 0
		render_text(screen, messagefont, messages[currentmessage], MESSAGE_X, MESSAGE_Y, messagecolors[currentmessage], MESSAGE_ALIGN)
	
	# blit the dead air image after doing everything above
	# dead air image could be partially transparent
	if mode == DEADAIR:
		screen.blit(surf_deadair, (0, 0))
	
	pygame.display.flip()
	
	# process events
	events = pygame.event.get()
	for event in events:
		if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
			done = True
	
	# delay
	time.sleep(0.1)

if USE_PIDFILE and DELETE_PIDFILE_ON_EXIT:
	os.remove(PIDFILE)

sys.exit(0)

