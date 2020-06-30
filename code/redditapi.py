import requests as req
import time
import os
import pandas as pd

sub_reddits =['CoronavirusUS','Coronavirus'] 
sub_fields = ['title', 
             'selftext',
             'subreddit', 
             'created_utc', 
             'author', 
             'num_comments', 
             'score', 
             'is_self']

# Least restrictive.Narrowing it down further doesn't get lot of results
# search_srting format is "abc""abc""abc"
search_string = "California"
day = 1
api_url = 'https://api.pushshift.io/reddit/search/submission?'
req_params = {'size': 500 }

for index in range(0,len(sub_reddits)):
	fname = 'subreddit_'+sub_reddits[index]
	reddit_posts = pd.DataFrame()
	for i in range(1,60):
		req_params['subreddit'] = sub_reddits[index]
		req_params['after'] = str(day * i)+'d'
		req_params['q'] = search_string
		# comma after being encoded causes call to fail.Maybe @Todo later
		#req_params['fields'] = fields 
		response = req.get(api_url,params = req_params)
		print(response.url)
		print("Day #", i)
		print("*******")
		assert response.status_code == 200
		json_resp = response.json()['data']
		#append to data frame only if we get any results back 
		if json_resp:
			print("Here")
			x = pd.DataFrame(json_resp)[sub_fields]
			print(x)
			reddit_posts = reddit_posts.append(x,ignore_index = True)
			del x #Re-declare to prevent duplication of data
		time.sleep(10)
	reddit_posts.to_csv(os.curdir+os.sep+fname+'.csv',index = False)
	del reddit_posts #Redeclare in for loop to avoid duplication of data

#https://api.pushshift.io/reddit/search/submission/?q="California""BayArea"&subreddit=CoronavirusUS

#https://api.pushshift.io/reddit/search/submission/?q="California""Bay Area"&subreddit=Coronavirus