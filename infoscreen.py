#!/usr/bin/env python

# Copyright (c) 2009 - 2013 Thomas Preece
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
import json

import pygame
from pygame.locals import *

import config
from config import *

# debug mode, no gfx
DEBUG = 0

# constants
NORMAL = 0
DEADAIR = 1

COLON = 10
MINUS = 11

# globals
mode = NORMAL
currentmessage = 0
TRACKINFO = 0

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
	reload_info()

def reload_info():
	global info
	with open(INFO_FNAME) as file:
		info = json.load(file)
		for message in info["messages"]:
			colors = message["color"].strip().split(' ')
			message["color"] = (int(colors[0]), int(colors[1]), int(colors[2])) 

reload_info()

def reload_config():
	reload(config)

def render_text(screen, font, text, x, y, color, align=LEFT):
	surf = font.render(text, True, color)
	if align == RIGHT:
		x -= surf.get_width()
	elif align == CENTER:
		x -= (surf.get_width()/2)
	
	screen.blit(surf, (x, y))


if DEBUG:
	sys.exit()

# write a PID file

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
digitalfont = pygame.font.Font(CLOCK_FONT, DIGITAL_FONT_SIZE)
backtimerfont = pygame.font.Font(CLOCK_FONT, BACKTIMER_FONT_SIZE)
npfont = pygame.font.Font(TEXT_FONT, NP_FONT_SIZE)
remainsfont = pygame.font.Font(REMAINS_FONT, REMAINS_FONT_SIZE)
onairfont = pygame.font.Font(ONAIR_FONT, ONAIR_FONT_SIZE)

dot_red = pygame.image.load(IMAGE_DIR+'/dot.png')

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

while True:	
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
		
	# draw clock with font
	if SHOW_DIGITAL:
		if DIGITAL_SECONDS:
			digitalstr = time.strftime("%H:%M:%S")
		else:
			digitalstr = time.strftime("%H:%M")

		render_text(screen, digitalfont, digitalstr, DIGITAL_X, DIGITAL_Y, COLOR['DIGITAL'], CENTER)

	# draw backtimer
	if SHOW_BACKTIMER:
		minsleft = 59 - mins
		secsleft = 60 - secs
		if secsleft==60:
			secsleft = 0
			minsleft += 1
		if minsleft==60:
			minsleft = 0

		if BACKTIMER_MINUS:
			backtimerstr = "-%02d:%02d" % (minsleft, secsleft)
		else:
			backtimerstr = "%02d:%02d" % (minsleft, secsleft)

		render_text(screen, backtimerfont, backtimerstr, BACKTIMER_X, BACKTIMER_Y, COLOR['BACKTIMER'], CENTER)


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
		
		render_text(screen, timefont, timestr, TIME_TEXT_X, TIME_TEXT_Y, COLOR['TIME'], TIME_TEXT_ALIGN)
	
	# draw date text
	if SHOW_DATE_TEXT:
		datestr = time.strftime(DATE_TEXT_FORMAT)
		render_text(screen, datefont, datestr, DATE_TEXT_X, DATE_TEXT_Y, COLOR['DATE'], DATE_TEXT_ALIGN)
	
	# draw message text
	if SHOW_MESSAGES:
		count += 1
		if count == TICKS_PER_MESSAGE:
			count = 0
			currentmessage += 1
			if currentmessage >= len(info["messages"]):
				currentmessage = 0
		render_text(screen, messagefont, info["messages"][currentmessage]["text"], MESSAGE_X, MESSAGE_Y, info["messages"][currentmessage]["color"], MESSAGE_ALIGN)

	# draw show/onair info
	if SHOW_ONAIR:
		if TRACKINFO:
			ONAIR_Y = HEIGHT - PROGRESS_BAR_HEIGHT - 40
		else:
			ONAIR_Y = HEIGHT - 40
		onair = TYPE[info["type"]] % str(info["onair"])
		render_text(screen, onairfont, info["show"], 15, ONAIR_Y, COLOR['SHOW'], LEFT)
		render_text(screen, onairfont, onair, WIDTH-15, ONAIR_Y, COLOR['ONAIR'], RIGHT)

	# NOW PLAYING stuff
	#
	start = int(info["track"]["start"])
	end = int(info["track"]["end"])
	if (time.time() < end) and (SHOW_PROGRESS or SHOW_TRACKINFO or SHOW_REMAINING):
		TRACKINFO = 1
		length = end - start
		played = time.time() - start
		remains = end - time.time()
		m, s = divmod(remains, 60)
		progress = played / float(length)

		if SHOW_PROGRESS:
			pygame.draw.rect(screen, COLOR['PROGRESS_BG'], pygame.Rect(0,HEIGHT-PROGRESS_BAR_HEIGHT,WIDTH,PROGRESS_BAR_HEIGHT))
			pygame.draw.rect(screen, COLOR['PROGRESS_FG'], pygame.Rect(0,HEIGHT-PROGRESS_BAR_HEIGHT,WIDTH*progress,PROGRESS_BAR_HEIGHT))

		if SHOW_TRACKINFO:
			trackinfostr = info["track"]["artist"] + " - " + info["track"]["title"]
			render_text(screen, npfont, trackinfostr, 12, HEIGHT-(PROGRESS_BAR_HEIGHT/1.2), COLOR['TRACK_INFO'], LEFT)
	
		if SHOW_REMAINING:
			remainingstr = "%d:%02d" % (m, s)
			render_text(screen, remainsfont, remainingstr, WIDTH-15, HEIGHT-(PROGRESS_BAR_HEIGHT/1.4), COLOR['TRACK_REMAINS'], RIGHT)
	
	else:
		TRACKINFO = 0

	# blit the dead air image after doing everything above
	# dead air image could be partially transparent
	if mode == DEADAIR:
		screen.blit(surf_deadair, (0, 0))
	
	pygame.display.flip()
	
	# process events
	events = pygame.event.get()
	for event in events:
		if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
			if USE_PIDFILE and DELETE_PIDFILE_ON_EXIT:
				os.remove(PIDFILE)
			sys.exit(0)
		if ((event.type == KEYUP) and (event.key == K_r)):
			reload_info()
			reload(config)
			from config import *
	
	# delay
	time.sleep(0.1)





