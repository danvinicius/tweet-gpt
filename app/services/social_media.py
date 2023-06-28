# Configurações de variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()
from os import environ

# Lib do twitter
import tweepy
twitter_client = tweepy.Client(environ['BEARER_TOKEN'])

class SocialMedia:
    def __init__(self):
        self.client = twitter_client

    def fetch_from_twitter(self, tag):
        try:
            tweets = twitter_client.search_recent_tweets(tag)
            id_primeiro_tweet = tweets.data[0].id
            corpo_do_tweet = self.client.get_tweet(id_primeiro_tweet).data.text
            return [id_primeiro_tweet, corpo_do_tweet]
        except:
            print('Erro ao buscar tweets.')
