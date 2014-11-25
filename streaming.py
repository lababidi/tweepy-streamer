#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import datetime, os, errno, argparse, json
# grab twitter auth tokens from external file
from tokens import *
import time


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):
        self.tweets = []
        self.folder = args.folder
        self.size = args.size
        self.counter = 0


    def on_data(self, data):
        js = json.loads(data.decode('utf-8'))
        if 'text' in js:
            print self.counter, js['text']
            self.tweets.append(data)
            self.counter += 1
            if self.counter > int(self.size):
                with open(self.folder + '/' + str(time.time()).split(".")[0], 'a') as f:
                    f.write('\n'.join(self.tweets).encode('UTF-8'))
                    self.counter = 0
                    del self.tweets[:]
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Stream from Twitter')
    argparser.add_argument('--lang',  default='', 
            help='language code, comma sep (ie en,jp)')
    argparser.add_argument('--token', default='0', 
            help='token to use', type=int)
    argparser.add_argument('--size', default=1000, 
            help='size of filesize batch', type=int)
    argparser.add_argument('--geo', default='', 
            help='geo bounding box, comma sep, long,lat,long,lat')
    argparser.add_argument('--track', default='', 
            help='words to track, comma sep')
    argparser.add_argument('--folder', required=True, 
            help='folder name to place tweets')

    args = argparser.parse_args()

    if len(args.geo)>0: geo = map(float,args.geo.split(','))
    else: geo = ''
#    if len(args.track)>0: track = args.track
#    else: track = ''
    access_token, access_token_secret = tokens[args.token]
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    mkdir_p(args.folder)

    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(track=[args.track], languages=[args.lang],locations=geo)
