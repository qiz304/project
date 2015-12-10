import re
import json
import csv
from geopy.geocoders import Nominatim
import ast

geolocator = Nominatim()


def find_tweet_address(gps_polygon_text):
    """
    Get details about the location of origin of a tweet
    based on GPS coordinates
    """
    location_dict = None
    gps_polygon_dict = ast.literal_eval(gps_polygon_text)
    longitude =  gps_polygon_dict['coordinates'][0][0][0]
    latitude =  gps_polygon_dict['coordinates'][0][0][1]
    tweetlocation = geolocator.reverse((latitude, longitude))
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
    print location_dict
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
        location_data = find_tweet_address(coords)
        try:
            state = location_data['state']
        except:
            state = ''
        tweet_dict = dict(tweetid=tweetid, userid=userid, place=place, coords=coords, country=country, state=state, lang=lang,
                         timestamp=timestamp, ttext=ttext, ttext_cleand=ttext_cleand)
        # print "\n", tweet_dict['ttext'], "\n", tweet_dict['ttext_cleand'], "\n", tweet_dict['state']
    else:
        pass
    return tweet_dict


def main():
    """

    :rtype : object
    """
    line_count = 0
    with open(incsvfile) as data_file:
        data = csv.reader(data_file)
        #data = data_file.xreadlines()
        #data = data_file.read()
        with open(outjsonfile, 'w') as fp:
            fp.write('[' + '\n')
            for tweet_data in data:
                tweet_dict = parsecsv(tweet_data)
                out_put = json.dumps(tweet_dict)
                if out_put != 'null':
                    if line_count == 0:
                        fp.write(out_put + '\n')
                    else:
                        fp.write("," + out_put + '\n')
                    line_count = 1
            fp.write(']' + '\n')


if __name__ == "__main__":
    incsvfile = raw_input("what is your input csv file name? ")
    outjsonfile = raw_input("what is your output json file name? ")
    main()

