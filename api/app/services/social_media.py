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
            # ID do Brasil
            tweets = self.client.search_tweets(tag, geocode="-14.2350,-51.9253,2000km")
            id_primeiro_tweet = tweets[0].id
            corpo_do_tweet = api.get_status(id_primeiro_tweet)
            print(corpo_do_tweet.text, id_primeiro_tweet)
            return [id_primeiro_tweet, corpo_do_tweet.text]
        except:
            print('Erro ao buscar tweets.')
