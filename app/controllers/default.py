from flask import request, jsonify
from app import app

# Configurações de variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()
from os import environ

# Lib do twitter
import tweepy

client = tweepy.Client(environ['BEARER_TOKEN'])

def analise_chat_gpt():
    return 'Análise braba'

# ex: http://localhost:5000/search?tag=brasil
@app.route('/search')
def search_tweet():
    try:
        query = request.args.get('tag')
        tag = '#' + query

        tweets = client.search_recent_tweets(tag)
        id_primeiro_tweet = tweets.data[0].id
        corpo_do_tweet = client.get_tweet(id_primeiro_tweet).data.text

        return jsonify(
            {
                'res': {
                    'tag': tag,
                    'tweet_id': id_primeiro_tweet,
                    'tweet_text': corpo_do_tweet,
                    'analise': analise_chat_gpt(),
                }
            }
        )
    except:
        return jsonify({'res': 'Houve um erro. Tente novamente mais tarde.'})
