
import sys
import datetime, calendar
import time
import pandas as pd
import os
import numpy as np
from twitterscraper import query_tweets

query_list = [
    'COVID',
    'COVID-19',
    'Corona',
    'Coronavirus',
    'Quarantine',
    '#COVID',
    '#COVID-19',
    '#quarantine',
    '#Quarantine',
    '#covid19'
]

''' 
DSI-SF Created additional variables for batching function
'''
tweet_months = [3,4,5]
tweet_year = [2020]

tweet_lat_lon = [ [37.7749,-122.194, 'SF'],
                  [34.0522,-118.2437, 'LA'],
                  [35.371652,-119.019531,'BAKERSFIELD']
                  [38.5816, -121.4944, "SAC"],
                  [32.7157, -117.1611, "SD" ],
                  [40.5865, -122.3917, "REDDING"]
            ] 
lat_lon_radius = '40mi'
f_name ='tweet'
f_extension = '.csv'

'''
get_tweets and get_tweets_geoloc are provided by DSI-NY cohort.
Modified both functions to use list of dictionary instead of nested dictionary
and to create a DF and write DF to csv instead of concatening to a DF & then 
writing to csv to speed up the functions a bit.
'''

#Get tweets without geolocation
def get_tweets(query, year, month, day,endday,loc): 
    tweets = []
    for query in query_list:
        for tweet in query_tweets(query,begindate=datetime.date(year,month,day),\
                                enddate=datetime.date(year,month,endday)):
            chirp = {} 
            chirp['tweet_id'] = tweet.tweet_id
            chirp['username'] = tweet.username
            chirp['text'] = tweet.text
            chirp['tweet_url'] = 'https://twitter.com'+tweet.tweet_url  
            chirp['tweet_date'] = tweet.timestamp
            chirp['hashtag'] = tweet.hashtags
            chirp['search_term'] = query
            chirp['city'] = np.NaN 
            chirp['lat'] = np.NaN
            chirp['long'] = np.NaN
            chirp['radius'] = np.NaN
            tweets.append(chirp)
        df = pd.DataFrame(tweets)
    df.to_csv(os.curdir+os.sep+f_name+'_'+loc+'_'+str(month)+'_'\
        +str(day)+'_'+str(endday)+f_extension,index = False)

def get_tweets_geoloc(query,lat,lon,radius,year,month,day,endday,loc): 
    tweets = []
    for query in query_list:
        for tweet in query_tweets(f"{query},geocode:{lat},{lon},{radius}",\
            begindate=datetime.date(year,month,day),\
            enddate=datetime.date(year,month,endday)):
            chirp = {} 
            chirp['tweet_id'] = tweet.tweet_id
            chirp['username'] = tweet.username
            chirp['text'] = tweet.text
            chirp['tweet_url'] = 'https://twitter.com'+tweet.tweet_url              
            chirp['tweet_date'] = tweet.timestamp
            chirp['hashtag'] = tweet.hashtags
            chirp['search_term'] = query
            chirp['lat'] = lat
            chirp['long'] = lon
            chirp['region'] = loc
            tweets.append(chirp)
        df = pd.DataFrame(tweets)
    df.to_csv(os.curdir+os.sep+f_name+'_'+loc+'_'+str(month)+'_'\
        +str(day)+'_'+str(endday)+f_extension,index = False)


''' 
DSI-SF Added batching of tweets as the twitterscrapper library opens too many
network connections without closing causing too many files open error. 
Batching also allows finer control over how many tweets we get 
'''

def batch_tweet_retrieval(f,batch_size_days = 13):
    '''
    For each location given in tweet_lat_lon list retrieve tweets for each month 
    using batch_size_days as the batch size. default can be overriden in 
    function call
    '''

    print(f"Calling function \033[1m{f.__name__}\033[0m\
            with batch size = \033[1m{batch_size_days}\033[0m\n")

    for index in range(len(tweet_lat_lon)):
        for m in tweet_months:
        #start from 1st day of the month
            flag = True
            end_day = 1
            date_range = str(datetime.date(tweet_year[0],m,end_day)).split('-')
            max_days = calendar.monthrange(tweet_year[0],m)[1]
            start_day = int(date_range[2])
            end_day = int(date_range[2]) + batch_size_days
            while flag: 
                if end_day >= max_days:
                    end_day = max_days
                    if f.__name__  == 'get_tweets_geoloc':
                        #query_list = query search string
                        #tweet_lat_lon[index][0] = lat
                        #tweet_lat_lon[index][1] = lon
                        #lat_lon_radius = geo location search radius in miles or km
                        #tweet_year = year
                        #m = month
                        #start_day = start date to get tweets for
                        #end_day = end date for get tweets for
                        #tweet_lat_lon[index][2] = two char code for location (optional)
                        f(
                        query_list,tweet_lat_lon[index][0],tweet_lat_lon[index][1],\
                        lat_lon_radius,tweet_year[0],m,\
                        start_day,end_day,tweet_lat_lon[index][2])
                    else:
                        f(query_list,tweet_year[0],m,start_day,end_day,tweet_lat_lon[index][2])
                    flag = False
                else:
                    if f.__name__  == 'get_tweets_geoloc':
                        f(
                        query_list,tweet_lat_lon[index][0],tweet_lat_lon[index][1],\
                        lat_lon_radius,tweet_year[0],m,\
                        start_day,end_day,tweet_lat_lon[index][2])
                    else:
                        f(query_list,tweet_year[0],m,start_day,end_day,tweet_lat_lon[index][2])
                    start_day = end_day
                    end_day = end_day + batch_size_days


batch_tweet_retrieval(get_tweets_geoloc)
#batch_tweet_retrieval(get_tweets)
