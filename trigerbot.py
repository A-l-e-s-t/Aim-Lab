from pynput.keyboard import Key, Controller, KeyCode
from pynput.keyboard import Listener as Keyboard_listener

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pyautogui
import win32api
import win32con
import win32gui
from win32gui import GetWindowText, GetForegroundWindow
from playsound import playsound
import pydirectinput
import sys
import time
import threading
import autoit
import ctypes
import datetime
import ait
import mouse
import numpy as nu
from mss import mss
import mss.tools
import mss

width, height = pyautogui.size()
cut_size = 0.0001 / 2
img_x1 = int(width * cut_size)
img_y1 = int(height * cut_size)
img_x2 = int(width * (1 - cut_size) - width * cut_size)
img_y2 = int(height * (1 - cut_size) - height * cut_size)
resize_width = int(width / 1)
resize_height = int(height / 1)

time.sleep(2.5)
playsound(
	'C:\\Users\\sergi\\Desktop\\Sounds\\A1-0002_sound_end00086413.wav')

fps_start_time = 0
fps = 0

while True:
	fps_end_time = time.time()
	time_diff = fps_end_time - fps_start_time
	fps = 1 / time_diff
	fps_start_time = fps_end_time
	# time.sleep(0.001)

	'''screenshot'''
	with mss.mss() as sct:
		monitor = {"top": img_y1, "left": img_x1,
							 "width": img_x2, "height": img_y2}

		# Grab the data
		img = sct.grab(monitor)
		img = Image.frombytes("RGB", img.size, img.bgra,
													"raw", "BGRX")
		# img.show()
		img = img.resize((resize_width, resize_height))
		# img.show()

	# time.sleep(9990.1)

	# (90, 145, 185)

	'''aim'''
	detected = []
	p = 30
	for x in range(resize_width):
		for y in range(resize_height):
			rgb_c = img.getpixel((x, y))
			r = rgb_c[0] + 0.001
			g = rgb_c[1] + 0.001
			b = rgb_c[2] + 0.001

			# blue
			c_r = 24
			c_g = 213
			c_b = 218

			# red
			# c_r = 180
			# c_g = 55
			# c_b = 50

			if (r - p <= c_r <= r + p) and (
					g - p <= c_g <= g + p) and (
					b - p <= c_b <= b + p):
				detected.append([x, y])

	cursor_x = int(resize_width / 2)
	cursor_y = int(resize_height / 2)
	enemies_x = 0
	enemies_y = 0
	if len(detected) > 0:
		for point in detected:
			enemies_x += point[0]
			enemies_y += point[1]
		enemy_x = int(enemies_x / len(detected))
		enemy_y = int(enemies_y / len(detected))

		distance_x = enemy_x - cursor_x
		distance_y = enemy_y - cursor_y

		# paint all groups on image
		pixels = img.load()
		print(group_center[0], group_center[1])
		pixels[group_center[0], group_center[1]] = (255, 255, 255)
		img.show()
		break

		# if distance_x and distance_y < 1:
		# 	autoit.mouse_down("left")
		# 	time.sleep(0.05)
		# 	autoit.mouse_up("left")

		multiplier = ((abs(distance_x) + abs(distance_y)) / (width + height)) * 50
		print(multiplier)
		# multiplier = 0.5

		win32api.mouse_event(
			win32con.MOUSEEVENTF_MOVE,
			int(distance_x * multiplier), int(distance_y * multiplier),
			0, 0)

	# print(f'fps {fps}, img.size {img.size}, detected {detected}')
	print(f'fps {fps}, img.size {img.size}')
