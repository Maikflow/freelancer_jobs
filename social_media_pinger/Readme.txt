-- Social Media Pinger --
Project Description:

A clearly documented python script to monitor FB likes,
Twitter followers, and Youtube channel subscribers and 
individual video views.

Details:
a. Script takes a csv file with four columns: uniq_id, account_handles, 
social_media (Twitter, FB, Youtube), frequency_of_scraping (No. of times/hr).
b. It handles errors gracefully - server not available etc.
- Tries again after some time.
- It writes errors to a log file - kind of error, time_stamp.
c. Uses the Twitter, FB, or Youtube API where available.
d. Outputs a csv that adds to the input_file, a column for each time. 


Instructions:

To succesfully run this script you're gonna need:
python 2.7, virtualenv, pip 

Installing python 2.7, pip and virtualenv: 
https://www.youtube.com/watch?v=Es_kdnPUgDg

Creating virtualenv: 
https://www.youtube.com/watch?v=yOeUKxVNQZU&spfreload=10

After installing and creating your virtualenv, run on command line: 
pip install -r requirements.txt 

You will also need to register apps for facebook, youtube and twitter:
https://developers.facebook.com/apps/
https://apps.twitter.com/
https://console.developers.google.com

Copy all the facebook and twitter keys onto options.ini
Download the google api keys in json format and put in directory as:
client_secrets.json

Main Script to run is Social_Media_Pinger.py

Google Authenthication (API V3) NOTES:
The first time running the script you will get prompted via webbrowser to authenticate the app, choose accept and this will create a new json file in the working directory called Social_Media_Pinger.py-oauth2.json.  

Input/output:

Input: SMP.csv
SMP.csv is a comma separated value file that can be viewed with popular office calc software (excel, libreCalc, etc)
Its headers are:
twitter_id	facebook_id	youtube_id	handle	social_media	scraping frequency (times/hour)	likes	followers	subscribers	video_views

Output: SMP.csv, error.log
Results are appended with a timestamp back to SMP.csv like so:
likes 2015-01-31 03:50:10	followers 2015-01-31 03:50:10	subscribers 2015-01-31 03:50:10

The error.log file contains all the tracebacks and exceptions thrown by the Social_Media_Pinger Class when accessing an API or any other exception. Can be set to debug to see all info for points of access and outputs. 


Dependencies:

facebook-sdk==1.0.0a0
google-api-python-client==1.3.1
httplib2==0.9
iso8601==0.1.10
oauth2client==1.4.6
oauthlib==0.7.2
pyasn1==0.1.7
pyasn1-modules==0.0.5
requests==2.4.3
requests-oauthlib==0.4.1
rsa==3.1.4
simplejson==3.6.5
six==1.9.0
tweepy==3.2.0
uritemplate==0.6
youtube-api-wrapper==0.2

	local modules
youtube_auth.py
config.Default_Ordered
