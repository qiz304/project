import sys
import re
import json
import csv
from geopy.geocoders import Nominatim
import ast
from time import sleep 
geolocator = Nominatim()


'''
input: twitter data file in CSV format
intermediate step: used command line grep "United States" tweets.csv 
output: JSON file with United States tweets only, state label added and tweet text cleaned

'''
 
 
def find_tweet_address(gps_polygon_text):
    """
    Get details about the location of origin of a tweet
    based on GPS coordinates
    """
    location_dict = None
    gps_polygon_dict = ast.literal_eval(gps_polygon_text)
    longitude =  gps_polygon_dict['coordinates'][0][0][0]
    latitude =  gps_polygon_dict['coordinates'][0][0][1]
    tweetlocation = geolocator.reverse((latitude, longitude), timeout=None)
    tweetaddress_fields = (tweetlocation.raw)
    try:
        county = tweetaddress_fields['address']['county']
        state = tweetaddress_fields['address']['state']
        zipcode = tweetaddress_fields['address']['postcode']
    except:
        county = ''
        state = ''
        zipcode = ''
    location_dict = dict(county=county, state=state, zipcode=zipcode)
    return location_dict
 

def tweet_cleaner(tweet):
    """
    tweet cleaning function
    adopted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    """
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

 
def parsecsv(tweet_data):
    """
    parse each tweet and extract values of interest
    """
    tweet_dict = None
    if tweet_data[3] == "United States":
        tweetid = tweet_data[-3]
        userid = tweet_data[-1]
        place = tweet_data[2]
        coords = tweet_data[1]
        country = tweet_data[3]
        lang = ''
        timestamp = tweet_data[-2]
        ttext = tweet_data[4]
        ttext_cleand = tweet_cleaner(ttext)
        sleep(1)
        location_data = find_tweet_address(coords)
        state = location_data['state']
        tweet_dict = dict(tweetid=tweetid, userid=userid, place=place, coords=coords, country=country, state=state, lang=lang,
                         timestamp=timestamp, ttext=ttext, ttext_cleand=ttext_cleand)
        # print "\n", tweet_dict['ttext'], "\n", tweet_dict['ttext_cleand'], "\n", tweet_dict['state']
    else:
        pass
    return tweet_dict
 
 
def main():
    """
 
    """
    line_count = 0
    #open the file in universal-newline mode
    with open(incsvfile, 'rU') as data_file:
        data = csv.reader(data_file)
        print ('[')
        for tweet_data in data:
            tweet_dict = parsecsv(tweet_data)
            out_put = json.dumps(tweet_dict)
            if out_put != 'null':
                if line_count == 0:
                    print (out_put)
                else:
                    print ("," + out_put)
                line_count = 1
        print (']')
 
 
if __name__ == "__main__":
    incsvfile = sys.argv[1]
    main()
 
