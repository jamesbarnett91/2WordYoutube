# Twitter bot which posts a random YouTube video based on a random adjective + noun search query
# Call from a cron job, or just manually for that artisanal, hand crafted feel
#
# 23/11/2014 jbarnett

import tweepy, urllib2, random, datetime, traceback
from bs4 import BeautifulSoup

def log(msg, sev='INFO'):
  with open('2wordyoutube.log', 'a') as f:
    f.write(datetime.datetime.now().isoformat() + ' - ' + sev + ': ' + msg + '\n')

class Video:
  def __init__(self, url, title):
    self.url = url
    self.title = title

CONSUMER_KEY = "xxx"
CONSUMER_SECRET = "xxx"
ACCESS_TOKEN = "xxx"
ACCESS_SECRET = "xxx"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# load wordlist
adjectives = []
with open("adjectives.txt", 'r') as f:
  for line in f:
    adjectives.append(line)

nouns = []
with open("nouns.txt", 'r') as f:
  for line in f:
    nouns.append(line)

adj = adjectives[random.randrange(0, len(adjectives))].strip(' \t\n\r')
noun = nouns[random.randrange(0, len(nouns))].strip(' \t\n\r')

try:
  # [URL, Title]
  videos = []

  resp = urllib2.urlopen("http://www.youtube.com/results?search_query=" + adj + "+" + noun).read()

  html = BeautifulSoup(resp)

  for title in html.body.find_all("a", { "class" : "yt-uix-tile-link"}):
    url = title['href']
    
    if (url.startswith("/watch")):
      videos.append(Video(url, title.text[:50] + '...'))

  if len(videos) > 0:
    target = videos[random.randrange(0,len(videos))]
    tweet =  adj + " " + noun + '\n\n' + 'Video Title: ' + target.title + '\n' + 'www.youtube.com' + target.url
    api.update_status(tweet)
    log(tweet.replace('\n', ' '), 'INFO')
  else:
    log(adj + ' ' + noun + ' found no results', 'ERR')

except urllib2.URLError, e:
  log(adj + ' ' + noun + ' caused: ' + e.reason, 'ERR')
except urllib2.HTTPError, e:
  log(adj + ' ' + noun + ' caused: ' + e.code, 'ERR')
except:
  log(adj + ' ' + noun + ' caused unexpected error:\n' + traceback.format_exc(), 'ERR')