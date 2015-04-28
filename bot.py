#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tweepy, time, sys
import config as cfg

argfile = str(sys.argv[1])

auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
auth.set_access_token(cfg.ACCESS_KEY, cfg.ACCESS_SECRET)
api = tweepy.API(auth)

filename=open(argfile,'r')
f=filename.readlines()
filename.close()

for line in f:
    api.update_status(status = line)
    #time.sleep(120)#Tweet every 2 minutes
    time.sleep(900)#Tweet every 15 minutes