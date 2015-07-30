import tweepy
import xlwt
from tagcloud import make_cloud

consumer_key = 'CrLQzqzOzUv9SkofOJjy7g' 
consumer_secret = 'whlfwFXArvUcLDsuqLqJUz3KKMuD9ZnEfBmylIBf4'
access_token = '1325364103-SrhmsMuglLuC9GRCgsXp9HgbsmNe4Lf2Ebe1RLP'
access_token_secret = 'cPu58QBGYLAljZpZNLYDl5G7FwzWPMHdLD4BQ7hTybQ'

handles = {'@epp':{'max':482537475341287423,'since':429322705356488704},
        '@greensep':{'max':483875192503271424,'since':429189226622488576},
        '@theprogressives':{'max':483885077282033663,'since':428810769590124544},
        '@martinschulz':{'max':484028730135052288,'since':429201864098598912},
        '@skakeller':{'max':483867581988999167,'since':429334477555662848},
        '@junckereu':{'max':485397624116486143,'since':428288824977158144},
        '@pes_pse':{'max':483522401968594944,'since':429270815931392001}}
hashtag = '#epp2014'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Display basic details for twitter user name
wb = xlwt.Workbook()
sheet_dict = {'platform':[5,0,'twitter'],'date_time':[5,1,'tweet.created_at'],'user':[5,2,'tweet.user.screen_name'],
              'text':[5,3,'tweet.text'], 'retweets':[5,4,'tweet.retweet_count']}

pages = 13
tweet_list = []

for handle in handles.keys():
    sheet1 = wb.add_sheet(handle)
    tweet_list = []
    x =0
    user = api.get_user(handle)
    # print ("Basic information for", user.name)
    print ("Screen Name:", user.screen_name)
    if handle == '@theprogressives':
        for page in range(1,pages):
            timeline = api.user_timeline(user_id=user.id,
                                         max_id=handles[handle]['max'],
                                         since_id=handles[handle]['since'],
                                         count=500,
                                         page=page)
            for tweet in timeline:
                x += 1
                if hashtag in tweet.text:
                    sheet1.write(5,5,hashtag)
                for key in sheet_dict.keys():
                    if sheet_dict[key][2] != 'twitter':
                        sheet1.write(sheet_dict[key][0]+x,sheet_dict[key][1],eval(sheet_dict[key][2]))
                    else:
                        sheet1.write(sheet_dict[key][0]+x,sheet_dict[key][1],sheet_dict[key][2])
                with open("hello.txt",'a') as file:
                    file.write(tweet.text.encode('utf8')+'\n')
                # print "Text:", tweet.text
                tweet_list.append(tweet.text.encode('utf8'))
                # print "ID:", tweet.id
                # print "User ID:", tweet.user.id
                # print "Created:", tweet.created_at
                # print "Retweeted:", tweet.retweeted
                # print "Retweet count:", tweet.retweet_count
        make_cloud(''.join(tweet_list),'/home/maikflow/Documents/python/twitter/wordclouds/'+handle)
# wb.save('tweets3.xls')