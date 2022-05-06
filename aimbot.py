# from pynput.keyboard import Key, Controller, KeyCode
# from pynput.keyboard import Listener as Keyboard_listener

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pyautogui
import win32api
import win32con
# import win32gui
# from win32gui import GetWindowText, GetForegroundWindow
from playsound import playsound
# import pydirectinput
# import sys
import time
import random
# import threading
import autoit
# import ctypes
# import datetime
# import ait
# import mouse
import numpy as nu
# from mss import mss
# import mss.tools
import mss

width, height = pyautogui.size()
cut_size = 0.75 / 2
img_x1 = int(width * cut_size)
img_y1 = int(height * cut_size)
img_x2 = int(width * (1 - cut_size) - width * cut_size)
img_y2 = int(height * (1 - cut_size) - height * cut_size)
resize_width = int(width / 100)
resize_height = int(height / 100)

time.sleep(1)
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
	detected_dist = {}
	# detected_dist['group 0'] = {}
	# detected_dist['group 1'] = {}
	# detected_dist['group 0']['points'] = [53, 3245]
	# detected_dist['group 1']['points'] = [67, 33444, 25]
	# detected_dist['group 2'] = {'points': [5432, 53]}
	# for point, group in enumerate(detected_dist.values()):
	# 	print(point, group)
	# detected_dist.insert(0, [5, 5])
	# group = detected_dist.index([])
	# print(list(detected_dist.values())[1])
	# detected_dist.update({f'group 1': [213412, 2345]})
	# detected_dist['group 1'].append([213412, 2345])
	# print(detected_dist)
	# break

	all_detected = []
	p = 80
	for x in range(resize_width):
		for y in range(resize_height):
			rgb_c = img.getpixel((x, y))
			r = rgb_c[0] + 0.001
			g = rgb_c[1] + 0.001
			b = rgb_c[2] + 0.001

			# blue
			# r1 = 0
			# g1 = 57
			# b1 = 65
			# r2 = 144
			# g2 = 255
			# b2 = 255

			# blue
			c_r = 24
			c_g = 213
			c_b = 218

			# red
			# c_r = 180
			# c_g = 55
			# c_b = 50

			# check if currently scanned point color same to needed color with bandwidth
			if (r - p <= c_r <= r + p) and (
					g - p <= c_g <= g + p) and (
					b - p <= c_b <= b + p):
				# if currently scanned point is first create new group
				if detected_dist == {}:
					detected_dist['group 0'] = {
						'points': [[x, y]], 'center': [], 'move': [], 'dist': 0
					}
				else:
					# get the closest detected point to currently scanned point
					closest_point = [[], 99 ** 99]
					for point in all_detected:
						dist_x = point[0] - x
						dist_y = point[1] - y
						dist = (abs(dist_x) + abs(dist_y))
						if closest_point[1] > dist:
							closest_point = [point, dist]
							if closest_point[1] == 0:
								break

					# if currently scanned point not close to any other point crate new group
					if closest_point[1] > 3:
						group = len(detected_dist)
						detected_dist[f'group {group}'] = {
							'points': [[x, y]], 'center': [], 'move': [], 'dist': 0
						}
					# else join to the closest group
					else:
						for group, points in enumerate(detected_dist):
							if closest_point[0] in detected_dist[f'group {group}']['points']:
								detected_dist[f'group {group}']['points'].append([x, y])
								break
				all_detected.append([x, y])

	if all_detected:
		# calculate dist from cursor to all groups
		cursor = (int(resize_width / 2), int(resize_height / 2))
		for group, points in enumerate(detected_dist):
			group_points = [0, 0]
			points = detected_dist[f'group {group}']['points']
			for point in points:
				group_points[0] += point[0]
				group_points[1] += point[1]

			group_center = [0, 0]
			group_center[0] = int(group_points[0] / len(points))
			group_center[1] = int(group_points[1] / len(points))

			group_dist = abs(
				abs(group_center[0] - cursor[0]) + abs(group_center[1] - cursor[1]))
			move_dist = [group_center[0] - cursor[0], group_center[1] - cursor[1]]
			detected_dist[f'group {group}']['center'] = group_center
			detected_dist[f'group {group}']['dist'] = group_dist
			detected_dist[f'group {group}']['move'] = move_dist

		closest_group = {'group': 0, 'dist': 99 ** 99}
		# all_groups_dist = []
		# for dist in detected_dist:
		# 	all_groups_dist.append(detected_dist['dist'])
		# closest_dist = min(all_groups_dist)
		# print(closest_dist)
		# for group in detected_dist:
		# 	print(group)
			# if group['dist'] == closest_dist:
			# 	closest_group =
		# all_groups_dist.append(detected_dist['dist'])
		for group, points in enumerate(detected_dist):
			if group == 0:
				closest_group = detected_dist[f'group {group}']
			# diff = abs(detected_dist[f'group {group}']['dist'] - closest_group[
			# 	'dist'])
			# print(diff)
			# if diff > 10:
			# 	closest_group = detected_dist[f'group {group}']
		# if detected_dist[f'group {group}']['dist'] < closest_group[
		# 	'dist']:
		# 	closest_group = detected_dist[f'group {group}']

		# if closest_group['dist'] < 2:
		# 	autoit.mouse_down("left")
		# 	time.sleep(0.05)

		# 	autoit.mouse_up("left")

		# print(closest_group)
		move = closest_group['move']
		# if closest_group['dist'] < 15:
		# 	# playsound(
		# 	# 	'C:\\Users\\sergi\\Desktop\\Sounds\\A1-0005_sound_tik00086455.wav')
		move[0] = closest_group['move'][0] * 2
		move[1] = closest_group['move'][1] * 2
		# multiplier = closest_group['dist'] / 10
		win32api.mouse_event(
			win32con.MOUSEEVENTF_MOVE, int(move[0]), int(move[1]), 0, 0)

		# paint all groups on image
		# pixels = img.load()
		# for group, points in enumerate(detected_dist):
		# 	rgb_c = (
		# 		random.randint(9, 255), random.randint(9, 255), random.randint(9, 255))
		# 	for point in detected_dist[f'group {group}']['points']:
		# 		pixels[point[0], point[1]] = rgb_c
		# 	group_center = detected_dist[f'group {group}']['center']
		# 	pixels[group_center[0], group_center[1]] = (255, 255, 255)
		# img.show()
		# break

		print(closest_group)
		print(f'img size {img.size}, fps {round(fps, 1)}'
					f', detected_dist {detected_dist}')
# print(f'img size {img.size}, fps {round(fps, 1)}')
