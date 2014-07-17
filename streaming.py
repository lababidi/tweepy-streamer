#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import datetime, os, errno, argparse, json
#grab twitter auth tokens from external file
from tw_tokens import tokens

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise
# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="puvoiy6Sb0o3RWK7GOIDVg"
consumer_secret="twgrBYX8K3mzVK6UwY2TfVUBtUVBtJrCzQKHo6c40"

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
			print js['text']
			self.tweets.append(data)
			self.counter+=1
			if self.counter>int(self.size):
				with open(self.folder+'/'+datetime.datetime.now().isoformat('_'),'a') as f:
					f.write(',\n'.join(self.tweets).encode('UTF-8'))
					self.counter = 0
					del self.tweets[:]
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Stream from Twitter')
	parser.add_argument('--lang','-l',default='')
	parser.add_argument('--track')
	parser.add_argument('--token',default='0')
	parser.add_argument('--size',default=1000)
	parser.add_argument('--folder', '-f')
	
	args = parser.parse_args()
	
	print args.lang
	access_token,access_token_secret=tokens[int(args.token)]
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	mkdir_p(args.folder)

	l = StdOutListener()
	stream = Stream(auth, l)
	stream.filter(track=[args.track],languages=[args.lang])
