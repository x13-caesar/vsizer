#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cv2
#import config


## moviepy version
'''
import moviepy.editor as mp

def resize(video, output, height):
	print('[-]Creating clip object...')
	clip = mp.VideoFileClip(video)
	print('[-]Resizing...')
	clip_resized = clip.resize(height=height) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
	print('[-]Writing file...')
	clip_resized.write_videofile(output, logger='bar')
'''

## ffmpeg version version 
import subprocess
def resize(video, output, height):
	video_in = video.replace(" ", "\\ ")
	video_out = output.replace(" ", "\\ ")
	subprocess.call(['ffmpeg-bar', '-i', video_in, '-c:v', 'libx264', '-preset', 'ultrafast', '-filter:v', 'scale=trunc(oh*a/2)*2:720', '-c:a', 'copy', '-y', video_out])


def resize_and_replace(movie_path, height):
	# Store initial movie file name and rename the file 
	indir, old_name = os.path.split(movie_path)
	new_name = old_name.split('.')[0]+'_initial.'+old_name.split('.')[1]
	new_path = os.path.join(indir, new_name)
	os.rename(movie_path, new_path)
	# Resize the movie, then delete the initial file
	try:
		resize(new_path, movie_path, height=height)
		if os.path.exists(movie_path):
			os.remove(new_path)
	# If failed, rename it back and record this failure
	except:
		os.rename(new_path, movie_path)
		# Print the failed files
		print('\033[0;31m[!]Failed file:\033[0m')


def movie_lists(root, escape_folder):
    for folder in escape_folder:
        if folder in root:
            return []
    total = []
    file_type = ['.mp4', '.avi', '.rmvb', '.wmv', '.mov', '.mkv', '.flv', '.ts', '.webm', '.MP4', '.AVI', '.RMVB', '.WMV','.MOV', '.MKV', '.FLV', '.TS', '.WEBM', '.iso','.ISO']
    dirs = os.listdir(root)
    for entry in dirs:
        f = os.path.join(root, entry)
        if os.path.isdir(f):
            total += movie_lists(f, escape_folder)
        elif os.path.splitext(f)[1] in file_type and '._' not in os.path.splitext(f)[0]:
            total.append(f)
    return total


if __name__ == '__main__':
	# Read config.ini
	#conf = config.Config(path='./config.ini')
	HEIGHT = 720

	# If processing single file, add the file path as the 1st parameter in command line
	if os.path.isfile(sys.argv[1]):
		movie_path = sys.argv[1]
		print('[+]Process single file:', os.path.split(movie_path)[1])

		resize_and_replace(movie_path, HEIGHT)

	else:
		movie_list = movie_lists(sys.argv[1], [])

		count = 0
		count_all = str(len(movie_list))
		print('[+]Find', count_all, 'movies')

		for movie_path in movie_list:  
			if os.path.split(movie_path)[1].startswith('._'):
				continue 
			count = count + 1
			percentage = str(count / int(count_all) * 100)[:4] + '%'
			print('\033[0;36m[!] - ' + percentage + ' [' + str(count) + '/' + count_all + '] -\033[0m')

			# If the movie is already small in height or width, skip it
			vid = cv2.VideoCapture(movie_path)
			h, w = vid.get(cv2.CAP_PROP_FRAME_HEIGHT), vid.get(cv2.CAP_PROP_FRAME_WIDTH)
			if os.path.getsize(movie_path) < 1000000000 or h <= 720 or w <=1280:
				print('[-]%s is small enough: %s MB' % (movie_path, os.path.getsize(movie_path)//1000000))
				continue
			resize_and_replace(movie_path, height=HEIGHT)


	print("\033[1;36m[+]All finished!!!\033[0m")
	input("\033[1;33m[+][+]Press enter key exit, you can check the error message before you exit.")




