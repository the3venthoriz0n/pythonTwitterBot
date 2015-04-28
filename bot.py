#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Andrew Kaplan Twitter Bot final project Social Software 4/28/15

'''
This bot selects a random location where there are trending topics,
chooses the top ten trending topics from that location,
then tweets about how it never would want to talk about those topics,
then follows all of it's followers back because it's lonely

'''

import tweepy, time, sys, random, collections
import config as cfg #import config file with authentication information

#----------------------AUTHENTICATION------------------------------------
auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
auth.set_access_token(cfg.ACCESS_KEY, cfg.ACCESS_SECRET)
api = tweepy.API(auth)

if  True: # api.verify_credentials():
	print "Your credentials are O.K."

	def _decode_list(data): #functions for decoding the unicode json object returned by the api.trends_available() method
	    rv = []
	    for item in data:
	        if isinstance(item, unicode):
	            item = item.encode('utf-8')
	        elif isinstance(item, list):
	            item = _decode_list(item)
	        elif isinstance(item, dict):
	            item = _decode_dict(item)
	        rv.append(item)
	    return rv

	def _decode_dict(data):
	    rv = {}
	    for key, value in data.iteritems():
	        if isinstance(key, unicode):
	            key = key.encode('utf-8')
	        if isinstance(value, unicode):
	            value = value.encode('utf-8')
	        elif isinstance(value, list):
	            value = _decode_list(value)
	        elif isinstance(value, dict):
	            value = _decode_dict(value)
	        rv[key] = value
	    return rv

	trendingPlaces = _decode_list(api.trends_available()) # convert unicode reply to normal utf-8 list, assign to variable trend
	trenDic = {}
	for item in trendingPlaces: #add name and yahoo world id for each item in trends list to dictionary of key value pairs
		trenDic[(item['name'])] = item['woeid']
		#print trenDic

	#topTen is a list containing dictionaries!
	topTen = _decode_list(api.trends_place((random.choice(trenDic.values())))) #choose random value(woeid)/place from dictionary(trenDic).
	
	try:
		for item in topTen: # iterate through items in topTen(list)
			for key in item:# iterate through keys in the dictionary within topTen
				if key == 'trends':
					topTenList = []
					topTenList = item.get(key) #fill list with values from key trends
		#print topTenList # list containing dictionaries of top ten trending for specific location
		topTenDic = {}
		for item in topTenList:
			topTenDic[(item['name'])] = item['url']
		print topTenDic
	except KeyError:
		print "Uhh oh! Key Error"



#-------------------OTHER IDEAS BELOW---------------------------------

	#follow every follower (A CRY FOR FRIENDSHIP!)
	# for follower in tweepy.Cursor(api.followers).items():
	#     follower.follow()

	#if api.exists_friendship(notTooPopular, user_b) # checks friendship, true if user a follows user b
	# api.followers_ids(id/screen_name/user_id) #returns id of followers 

	#     #time.sleep(120)#Tweet every 2 minutes
	#     time.sleep(900)#Tweet every 15 minutes (15*60)
else:
	print "Your credentials are incorrect! Check the config file"

























