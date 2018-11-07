import requests
import os
import json
import urllib.request

import constants

def get_client_id():
	secrets = json.load(open(constants.TWITCH_SECRETS_FILE))['client_id']
	return secrets

"""
	Fetch the amount of clips until we hit the limit.
"""
def get_top_clips(period, game, limit):
	response = fetch_top_clips(period, game, 100)
   
	# Retry if failed the first time. Twitch API has errors on the first call for some reason.
	if 'clips' not in response:
		response = fetch_top_clips(period, game, 100)

	return format_clips(response['clips'], limit)

def format_clips(clips, limit):
	formatted_clips = []
	counter = 0
	for clip in clips:
		if counter < limit:
			if is_clip_unique(clip, formatted_clips):
				if clip['broadcaster']['display_name'] not in constants.BLACKLISTED_CHANNELS:
					counter += 1
					formatted_clips.append({
						'title': clip['title'],
						'channel': clip['broadcaster']['display_name'],
						'url': 'https://clips.twitch.tv/' + clip['slug'],
						'slug': clip['slug'],
						'game': clip['game'],
						'date': clip['created_at'],
						'views': clip['views'],
						'duration': clip['duration'],
						'thumbnail': clip['thumbnails']['medium'],
						'vod': clip['vod']
					})
	return formatted_clips 

def get_mock_clips(limit):
	"""
		Fetch a clip from mock data for testing purposes.
	"""
	with open(constants.ASSETS_LOCATION + '/mockdata.json') as f:
		data = json.load(f)

	return format_clips(data['clips'], limit=limit)

def fetch_top_clips(period, game, limit):
	headers = {
		'Accept': 'application/vnd.twitchtv.v5+json',
		'Client-ID': get_client_id(),
	}

	params = (
		('period', period),
		('game', clean_text(game)),
		('limit', limit),
		('language', 'en')
	)

	response = requests.get('https://api.twitch.tv/kraken/clips/top', headers=headers, params=params)
	return response.json()

def download_clip(basedir, clip):
	channel = clip['channel']
	filename = clip['slug']
	outputpath = (basedir + channel + '/' + filename + '.mp4').replace('\n', '')

	# Create downloads directory if it doesn't exist already
	if not os.path.exists(basedir + channel + '/'):
		os.makedirs(basedir + channel + '/')

	mp4url = get_clip_mp4_url(clip['slug'])

	# Download file to output path
	print('Downloading: ' + mp4url + ' --> ' + outputpath)
	r = requests.get(mp4url)
	f = open(outputpath,'wb')
	for chunk in r.iter_content(chunk_size=255): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	f.close()

def get_clip_mp4_url(clip_slug):
	url = "https://clips.twitch.tv/api/v2/clips/" + clip_slug + "/status"
	response = requests.get(url)
	mp4url = get_mp4_url_by_quality(response.json(), '720')
	return mp4url

def get_mp4_url_by_quality(response, quality):
	"""
		Gets the chosen quality mp4 url from a Twitch status response.
		Example response: https://clips.twitch.tv/api/v2/clips/HorribleSpicyEelBIRB/status
	"""
	mp4url = None

	for qo in response['quality_options']:
		if qo['quality'] == quality:
			mp4url = qo['source']

	# Pick first option if quality isn't available.
	if mp4url is None:
		mp4url = response['quality_options'][0]['source']

	return mp4url

def clean_text(text):
	"""
		Clean the game string so it can be used in API calls.
	"""
	text = text.replace("_", " ")
	text = text.replace("%20", " ")
	text = text.replace("%S1", "'")

	return text

def is_clip_unique(clip, clips):
	"""
		Check if a clip is unique in a list of clips.
	"""
	# Auto add clips without VOD for now. No way to check if they are duplicates.
	if clip['vod'] == None:
		return True

	for c in clips:
		if c['vod'] is not None:
			if clip['vod']['id'] == c['vod']['id']:
				# Clip found with same VOD ID in list. Possible duplicate. Might be a clip from the same stream.
				# Check to see if the timestamps match to prevent duplicate clips.
				timestamp = extract_timestamp_from_vod_url(clip['vod']['url'])
				possibleDuplicateTimestamp = extract_timestamp_from_vod_url(c['vod']['url'])
				if timestamp == possibleDuplicateTimestamp:
					return False
	return True

def extract_timestamp_from_vod_url(vod_url):
	"""
		Extracts the timestamp from a twitch VOD URL.
	"""
	return extract_hours_and_minutes_from_timestamp(vod_url.split('?t=', 1)[1])

def extract_hours_and_minutes_from_timestamp(timestamp):
	return timestamp.split('m', 1)[0]