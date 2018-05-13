import requests
import os
import json
import urllib.request

import constants

def getTwitchClientID():
	secrets = json.load(open(constants.TWITCH_SECRETS_FILE))['client_id']
	return secrets

"""
	Fetch the amount of clips until we hit the limit.
"""
def getTwitchClips(period, game, limit):
	response = fetchTwitchClips(period, game, 100)

	# print(response)
   
	# Retry if failed the first time. Twitch API has errors on the first call for some reason.
	if 'clips' not in response:
		response = fetchTwitchClips(period, game, 100)

	clips = []
	counter = 0
	for clip in response['clips']:
		if counter < limit:
			if isClipUnique(clip, clips):
				if clip['broadcaster']['display_name'] not in constants.BLACKLISTED_CHANNELS:
					counter += 1
					clips.append({
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
	return clips 

def fetchTwitchClips(period, game, limit):
	headers = {
		'Accept': 'application/vnd.twitchtv.v5+json',
		'Client-ID': getTwitchClientID(),
	}

	params = (
		('period', period),
		('game', cleanGameText(game)),
		('limit', limit),
		('language', 'en')
	)

	response = requests.get('https://api.twitch.tv/kraken/clips/top', headers=headers, params=params)
	return response.json()

def downloadTwitchClip(basedir, clip):
	channel = clip['channel']
	filename = clip['slug']
	outputpath = (basedir + channel + '/' + filename + '.mp4').replace('\n', '')

	# Create downloads directory if it doesn't exist already
	if not os.path.exists(basedir + channel + '/'):
		os.makedirs(basedir + channel + '/')

	mp4url = getClipMp4Url(clip['slug'])

	# Download file to output path
	print('Downloading: ' + mp4url + ' --> ' + outputpath)
	r = requests.get(mp4url)
	f = open(outputpath,'wb')
	for chunk in r.iter_content(chunk_size=255): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	f.close()

def getClipMp4Url(clip_slug):
	url = "https://clips.twitch.tv/api/v2/clips/" + clip_slug + "/status"
	response = requests.get(url)
	mp4url = getMp4UrlByQuality(response.json(), '720')
	return mp4url

def getMp4UrlByQuality(response, quality):
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

def cleanGameText(game):
	"""
		Clean the game string so it can be used in API calls.
	"""
	game = game.replace("_", " ")
	game = game.replace("%20", " ")
	game = game.replace("%S1", "'")

	return game

def isClipUnique(clip, clips):
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
				timestamp = extractTimestampFromVODURL(clip['vod']['url'])
				possibleDuplicateTimestamp = extractTimestampFromVODURL(c['vod']['url'])
				if timestamp == possibleDuplicateTimestamp:
					return False
	return True

def extractTimestampFromVODURL(vod_url):
	"""
		Extracts the timestamp from a twitch VOD URL.
	"""
	return extractHoursAndMinutesFromTimestamp(vod_url.split('?t=', 1)[1])

def extractHoursAndMinutesFromTimestamp(timestamp):
	return timestamp.split('m', 1)[0]