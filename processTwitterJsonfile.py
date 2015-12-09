import json

#import regex
import re

'''
input: twitter data file in JSON format
output: JSON file with United States tweets only, state label added and tweet text cleaned

'''


#start process_tweet
def tweetcleaner(tweet):
    ''' function adopted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/'''
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end


def parsejson(tweet_data):
    tweet_dict = None
    if tweet_data["_source"]["place"]["country_code"] == "US":
        tweetid = tweet_data["_id"]
        userid = tweet_data["_source"]["user"]["id"]
        place = tweet_data["_source"]["place"]["full_name"]
        coords = tweet_data["_source"]["coordinates"]
        country = tweet_data["_source"]["place"]["country"]
        lang = tweet_data["_source"]["lang"]
        timestamp = tweet_data["_source"]["timestamp_ms"]
        ttext = tweet_data["_source"]["text"]
        ttext_cleand = tweetcleaner(ttext)
        state = place.strip()[-3:].strip()
        if state == 'USA':
            state = place.split(",")[0]
        else:
            state = state
            
        tweet_dict = dict(tweetid=tweetid, userid=userid, place=place, coords=coords, country=country, state=state, lang=lang,
                         timestamp=timestamp, ttext=ttext, ttext_cleand=ttext_cleand)
        #print "\n", tweetdict['ttext'], "\n", tweetdict['ttext_cleand'], "\n", tweetdict['state']
    else:
        pass
    return tweet_dict
 

def main():
    """

    :rtype : object
    """
    line_count = 0
    with open(injsonfile) as data_file:
        data = json.load(data_file)
    with open(outjsonfile, 'w') as fp:
        fp.write('[' + '\n')
        for tweet_data in data:
            tweet_dict = parsejson(tweet_data)
            out_put = json.dumps(tweet_dict)
            if out_put != 'null':
                if line_count == 0:
                    fp.write(out_put + '\n')
                else:
                    fp.write("," + out_put + '\n')
                line_count = 1
        fp.write(']' + '\n')


if __name__ == "__main__":
    injsonfile = raw_input("what is your input json file name? ")
    outjsonfile = raw_input("what is your output json file name? ")
    main()
