import json
import urllib.parse
import urllib.request
import socket
from collections import defaultdict
import datetime
import os
import sys
import re

YOUTUBE_API_KEY = ''

BASE_YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/videos?id='

def get_video_id(video_url):
	x = video_url.split("v=")[1]
	next_param_index = x.find('&')
	if next_param_index != -1:
		x = x[0:next_param_index]
	return x

def build_url(video_id):
	url = BASE_YOUTUBE_URL + video_id + '&key=' + YOUTUBE_API_KEY + '&part=snippet,contentDetails,statistics,status'
	return url

def get_contents(url):
	result = None
	try:
		result = urllib.request.urlopen(url)
		ans = json.loads(result.read().decode(encoding = 'utf-8'))
		return ans
	except Exception as e:
		print(str(e))
		exit()
	if result != None:
		result.close()

def _js_parseInt(string):
	return int(''.join([x for x in string if x.isdigit()]))

def YTDurationToSeconds(duration):
	match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
	hours = _js_parseInt(match[0]) if match[0] else 0
	minutes = _js_parseInt(match[1]) if match[1] else 0
	seconds = _js_parseInt(match[2]) if match[2] else 0
	return hours * 3600 + minutes * 60 + seconds

def parse_result(result):
	info = defaultdict()
	info["title"] = result["items"][0]["snippet"]["title"]
	info["thumbnail"] = result["items"][0]["snippet"]["thumbnails"]["default"]["url"]
	temp = result["items"][0]["contentDetails"]["duration"] 
	info["duration"] = YTDurationToSeconds(temp)
	return info

def get_title(info):
	return info["title"]

def get_thumbnail(info):
	return info["thumbnail"]

def get_duration(info):
	return info["duration"]
