#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import datetime, os, errno, argparse, json, geohash
from collections import Counter
#grab twitter auth tokens from external file
from tw_tokens import tokens
from dateutil import parser

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

def twitter_epoch(s):
	return unix_time(parser.parse(s).replace(tzinfo=None))
	# return datetime.datetime.strptime(s,'%a %b %d %H:%M:%S %z %Y')
	#"Wed Aug 27 13:08:45 +0000 2008"

def map_to_csv(mm):
	with open('map.csv','w') as f:
		for m,v in mm.most_common():
			f.write(m[0]+','+str(m[1])+','+str(v)+'\n')

def _to_json(t):
	with open('map.json','w') as f:
		f.write(json.dumps(t))

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="puvoiy6Sb0o3RWK7GOIDVg"
consumer_secret="twgrBYX8K3mzVK6UwY2TfVUBtUVBtJrCzQKHo6c40"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
counter = 0

heatmap = Counter()

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.
	"""
	def __init__(self): 
		self.tweets = []
		self.folder = args.folder
		self.size = args.size
		self.counter = 0
		self.map = Counter()
		self.time_geo = {}
		for n in range(0,60):
			self.time_geo[n] = Counter()

	def on_data(self, data):
		global counter
		js = json.loads(data.decode('utf-8'))
		if 'coordinates' in js and  js['coordinates']!=None:
			print js['coordinates']
			c = js['coordinates']['coordinates']
			print c
			g = geohash.encode(c[1],c[0])
			t = twitter_epoch(js['created_at'])
			#self.map[g[:5],(t/3600)%24]+=1
			self.map[g[:5],(t/60)%60]+=1
			self.time_geo[(t/60)%60][g[:5]]+=1
			self.counter+=1
			print self.counter
			print self.size
			print self.size<self.counter

		if self.counter>args.size:
			map_to_csv(self.map)
			_to_json(self.time_geo)
			self.counter = 0
			print 'writing to file'
		#if 'text' in js:
		# 	print js['text']
		# 	self.tweets.append(data)
		# 	self.counter+=1
		#	print self.counter
		# 	if self.counter>int(self.size):
		# 		with open(self.folder+'/'+datetime.datetime.now().isoformat('_'),'a') as f:
		# 			f.write(',\n'.join(self.tweets).encode('UTF-8'))
		# 			self.counter = 0
		# 			del self.tweets[:]
		return True

	def on_error(self, status):
		print status
		return False

if __name__ == '__main__':
	aparser = argparse.ArgumentParser(description='Stream from Twitter')
	aparser.add_argument('--lang','-l',default='')
	aparser.add_argument('--track',default='')
	aparser.add_argument('--token',default='0')
	aparser.add_argument('--size',default=1000, type=int)
	aparser.add_argument('--folder', '-f',required=True)
	aparser.add_argument('--geo', '-g')

	args = aparser.parse_args()

	print type(args.size)
	geo = map(float,args.geo.split(','))
	print geo
	access_token,access_token_secret=tokens[int(args.token)]
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	mkdir_p(args.folder)

	l = StdOutListener()
	stream = Stream(auth, l)
	stream.filter(track=[args.track],languages=[args.lang],locations=geo)
