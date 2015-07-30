#!/usr/bin/env python
__author__ = "Darflow"
"""
Project Description:

    A clearly documented python script to monitor FB likes,
    Twitter followers, and Youtube channel subscribers and 
    individual video views.

Details:

    a.  Script takes a csv file with four columns: uniq_id, account_handles, 
        social_media (Twitter, FB, Youtube), frequency_of_scraping (No. of times/hr).
    b.  It handles errors gracefully - server not available etc.
        - Tries again after some time.
        - It writes errors to a log file - kind of error, time_stamp.
    c.  Uses the Twitter, FB, or Youtube API where available.
    d.  Outputs a csv that adds to the input_file, a column for each time. 
"""

import os
import csv
import logging
from time import time
from ConfigParser import ConfigParser
from collections import defaultdict
from datetime import datetime

from Default_Ordered import DefaultOrderedDict

import facebook
import tweepy
from youtube_auth import get_authenticated_service
from oauth2client.tools import argparser, run_flow

class Social_Media_Tracker(object):
    """
    Track a single entity across 3 diferent types of social media:
    Facebook, Twitter and Youtube.

    As of now you can retrieve:
    -No. of likes from facebook
    -No. of followers from Twitter
    -No. of Subscribers from Youtube

    This class takes a CSV input file with the following header:
    twitter_id,  facebook_id, youtube_id,  handle, scraping frequency (times/hour),
    likes, followers, subscribers, video_views.

    It also has a configuration file (.ini) for FB and Twitter App keys.
    The Youtube pinger method has dependencies that reside in current directory.
    """

    def __init__(self, input_file='scrape_data.csv', config='options.ini'):
        self.input_file = input_file
        self.data_dict = DefaultOrderedDict(list)
        ts = time()
        self.stamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.read_csv()
        options = os.path.join(os.path.dirname(__file__),config)
        self.config = ConfigParser()
        self.config.read(options)

    def read_csv(self):
        """Loads input csv file into memory as dict"""
        with open(self.input_file, 'r') as f:
            self.data = csv.DictReader(f)
            for header in self.data.fieldnames:
                self.data_dict[header] = []
            for row in self.data:
                for key,value in row.iteritems():
                    self.data_dict[key].append(value)

    def write_csv(self):
        """Writes back to csv file"""
        with open(self.input_file, 'wb') as f:
            writer = csv.writer(f)
            values = self.data_dict.values()

            writer.writerow(self.data_dict.keys())
            for vals in range(len(values[0])):
                writer.writerow([row[vals] for row in values])

    def log_error(self, origin):
        """Logs error into txt file for debugging"""
        logging.basicConfig(filename='error.log',level=logging.WARNING,
                format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('Warning: ')
        logging.exception('ping {} method error: '.format(origin))

    def ping_facebook(self, *args, **kwargs):
        """pings facebook for number of likes in current time"""

        #Facebook API authentication procedure
        token = self.config.get('facebook','token')
        graph = facebook.GraphAPI(token)

        #Look up number of likes from facebook_id written in csv
        for i,ID in enumerate(self.data_dict['facebook_id']):
            try:
                node = graph.get_object(ID)
                print 'facebook likes:', node['likes'], i
                if i>0:
                    self.data_dict['likes '+self.stamp].append(node['likes'])
                else:
                    self.data_dict['likes '+self.stamp] = [node['likes']]
            except Exception, error:
                self.log_error('facebook')
        print self.data_dict

    def ping_twitter(self, *args, **kwargs):
        '''pings twitter for follower_count information'''

        #Twitter API authentication process
        #App credentials obtained from external .ini file
        client_id = self.config.get('twitter','client_id')
        client_secret = self.config.get('twitter', 'client_secret')
        token = self.config.get('twitter','token')
        token_secret = self.config.get('twitter','token_secret')
        auth = tweepy.OAuthHandler(client_id, client_secret)
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)

        #Look up twitter id in csv and write new follower_count
        for i,ID in enumerate(self.data_dict['twitter_id']):
            try:
                user = api.get_user(auth, ID)
                print 'number of followers:',user.followers_count
                self.data_dict['followers'][i] = user.followers_count
                if i>0:
                    self.data_dict['followers '+self.stamp].append(user.followers_count)
                else:
                    self.data_dict['followers '+self.stamp] = [user.followers_count]
            except Exception, error:
                self.log_error('twitter')
    
    def ping_youtube(self, *args, **kwargs):
        '''pings youtube for number of subscribers on a given channel ID'''

        #Youtube API V3 authentication
        #External modules and dependencies are required
        argparser.add_argument("--message", required=False,
                    help="Text of message to post.")
        args = argparser.parse_args()
        youtube = get_authenticated_service(args)

        #Get statistics from channel id 
        for i,ID in enumerate(self.data_dict['youtube_id']):
            try:
                subs = youtube.channels().list(part="statistics", 
                    id=ID).execute()
                print 'No. of subscribers:',subs['items'][0]['statistics']['subscriberCount']
                if i>0:
                    self.data_dict['subscribers '+self.stamp].append(subs['items'][0]['statistics']['subscriberCount'])
                else:
                    self.data_dict['subscribers '+self.stamp] = [subs['items'][0]['statistics']['subscriberCount']]
            except Exception, error:
                self.log_error('youtube')
        print self.data_dict

if __name__ == "__main__":
    tracker = Social_Media_Tracker()
    tracker.ping_facebook()
    tracker.ping_twitter()
    tracker.ping_youtube()
    tracker.write_csv()
