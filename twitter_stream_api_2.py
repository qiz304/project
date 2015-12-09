from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

ckey = ''
csecret = ''
atoken = ''
asecret = ''

oauth = OAuth(atoken, asecret, ckey, csecret)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(locations='-126,-58,26,50', lang='en')

print "\nHow many tweets would you like to collect?"
tweet_count = input()
with open('tweets.csv','w') as tweet_file:
	final_dict = {'uid':[], 'tid':[], 'text':[], 'timestamp':[], 'city':[], 'country':[], 'bounding_box':[]}
	for tweet in iterator:
		tweet_count -= 1
		# Twitter Python Tool wraps the data returned by Twitter 
		# as a TwitterDictResponse object.
		# We convert it back to the JSON format to print/score
		tweet.values()
		for k,v in tweet.iteritems():
			if k == 'text':
				final_dict['text'].append(v)
			elif k == 'user':
				final_dict['uid'].append(v['id'])
			elif k == 'id':
				final_dict['tid'].append(v)
			elif k == 'timestamp_ms':
				final_dict['timestamp'].append(long(v))
			elif k == 'place':
				try:
					final_dict['city'].append(v['full_name'].split(',')[0])
					final_dict['country'].append(v['country'])
					final_dict['bounding_box'].append(v['bounding_box'])
				except:
					final_dict['city'].append('')
					final_dict['country'].append('')
					final_dict['bounding_box'].append('')


		if tweet_count <= 0:
			break

	
	tweet_df = pd.DataFrame(final_dict)
	tweet_df.to_csv(tweet_file)

