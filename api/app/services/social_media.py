# Configurações de variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()
from os import environ

consumer_key = environ['consumer_key']

consumer_secret = environ['consumer_secret']

access_token = environ['access_token']

access_token_secret = environ['access_token_secret']

# Lib do twitter
import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create the API object
api = tweepy.API(auth)

class SocialMedia:
    def __init__(self):
        self.client = api

    def fetch_from_twitter(self, tag):
        try:
            tweets = self.client.search_tweets(tag, geocode="-14.2350,-51.9253,1500km", tweet_mode='extended')
            return [tweets[0].id, tweets[0].full_text, tweets[0].user.screen_name, tweets[0].created_at]
        except:
            print('Erro ao buscar tweets.')
