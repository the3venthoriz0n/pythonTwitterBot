#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Andrew Kaplan Twitter Bot final project Social Software 4/28/15

'''
This bot selects a random location where there are trending topics,
chooses the top ten trending topics from that location,
then tweets lines from the raven by Edgar Allan Poe, comparing them to the trending topics,
then follows all of it's followers back because it's lonely

'''

import tweepy, time, sys, random, collections
import config as cfg #import config file with authentication information

argfile = str(sys.argv[1]) # pass text file to command line argument

#----------------------AUTHENTICATION------------------------------------
auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
auth.set_access_token(cfg.ACCESS_KEY, cfg.ACCESS_SECRET)
api = tweepy.API(auth)
myUID = 2912975613 # my user identification number


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

	def updateStatus(trend, place, text):
		#updtate twitter status with passed in values
		trend = trend.replace(" ", "") # remove all spaces
		trend = trend.replace("#", "") # remove hashtag if it exists, so I can place my own
		place = place.replace(" ", "") # remove all spaces from string
		status = text + "...SO much better than " + " #" + trend + " in" + " #" + place
		api.update_status(status = status)
		print "\n", "Status updated!"

	filename = open(argfile,'r')#open file, with argument r for read
	fileLines = filename.readlines()# read random line into variable f
	filename.close()#close file reader

#----------------------FOLLOW MY FOLLOWERS (a cry for friendship)-------------------------------------

	myFollowers = api.followers_ids(myUID) #returns id of followers, by default of authenticated account. my info: 2912975613 (the3venthoriz0n)
	print "\n", "MY FOLLOWERS: ", myFollowers
	if len(myFollowers) > 0: #check that followers exist
		for follower in myFollowers: #iterate through followers
			api.create_friendship(follower)
			print "I just followed: ", follower

#--------------------------------------START TRENDS CODE--------------------------------------------------
	for line in fileLines: #loop this code every loopInterval
		trendingPlaces = _decode_list(api.trends_available()) # convert unicode reply to normal utf-8 list, assign to variable trend
		trendPlaceDic = {}
		for item in trendingPlaces: #add name and yahoo world id for each item in trends list to dictionary of key value pairs
			trendPlaceDic[(item['name'])] = item['woeid']
			#print "trendPlaceDic: ", trendPlaceDic

		#topTen is a list containing dictionaries as elements!
		randomPlaceName = random.choice(trendPlaceDic.keys())#random key from trendPlaceDic
		randomWoeid = trendPlaceDic.get(randomPlaceName) # choose value coresponding to key in trending places dictionary
		topTen = _decode_list(api.trends_place(randomWoeid)) #get top tend trends from value(woeid)/place from dictionary(trenPlaceDic)
		try:
			for item in topTen: # iterate through items in topTen(list)
				for key in item:# iterate through keys in the dictionary within topTen
					if key == 'trends':
						topTenList = []
						topTenList = item.get(key) #fill list with values from key trends
			#print "topTenList: ", topTenList # list containing dictionaries of top ten trending for specific location
			topTenDic = {}
			for item in topTenList:
				topTenDic[(item['name'])] = item['url']
			#print "topTenDIc: ", topTenDic
		except KeyError:
			print "Uhh oh! Key Error"
		randomTrend = random.choice(topTenDic.keys())
		updateStatus(randomTrend, randomPlaceName, line) #update status with line from textfile
		time.sleep(15 * 60)# in seconds, run code/tweet every 15 minutes

	# #old status update
	# statusUpdate = "I wouldn't be caught dead talking about " + randomTrend + " are you kidding me?!"		
	# api.update_status(status = statusUpdate)
	# print "Status updated!"	
else:
	print "Your credentials are incorrect! Check the config file"


	#-------------------OTHER IDEAS BELOW---------------------------------

			# to read line differently? Doesnt work
			# i = 0 
			# while i in range(0, len(fileLines)):
			# 	line = fileLines[i]
			# 	updateStatus(randomTrend, randomPlaceName, line)#update status with line from f
			# 	i += 1
			# 	if i >= len(fileLines): #restart reading file once reached end
			# 		i = 0

			# #another method, follow every follower 
			# for follower in tweepy.Cursor(api.followers).items():
			#     follower.follow()
			#friends = api.show_friendship(source_id = myUID, target_id = follower)	# get friendship info
			# print "Friends: ",friends 

			#create dictionary of friend objects (not very useful since cant iterate over friend object)
			# counter = 0
			# for item in friends:
			# 	fDic = {}
			# 	fDic[counter] = item #create key value pairs, key is counter, value is item
			# 	counter += 1
			#print "\n", "FDIC TEST: ", fDic

		#     #time.sleep(120)#Tweet every 2 minutes
		#     time.sleep(900)#Tweet every 15 minutes (15*60)






















