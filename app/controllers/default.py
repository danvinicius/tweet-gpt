from flask import request, jsonify
from app import app

# Configurações de variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()
from os import environ

# Lib do twitter
import tweepy

#Lib do chatgpt
import openai

openai.api_key = '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'

twitter_client = tweepy.Client(environ['BEARER_TOKEN'])

def analise_chat_gpt(text):
    chat_input = [
        {'role': 'user', 'content': 'Quero que você comente de maneira cômica o seguinte texto'},
        {'role': 'assistant', 'content': 'Beleza, qual é o texto?'},
        {'role': 'user', 'content': text}
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_input
    )
    assistant_reply = response['choices'][0]['message']['content']
    
    return assistant_reply


# ex: http://localhost:5000/search?tag=brasil
@app.route('/search')
def search_tweet():
    try:
        query = request.args.get('tag')
        tag = '#' + query

        tweets = twitter_client.search_recent_tweets(tag)
        id_primeiro_tweet = tweets.data[0].id
        corpo_do_tweet = twitter_client.get_tweet(id_primeiro_tweet).data.text
        
        analise = analise_chat_gpt(corpo_do_tweet)

        return jsonify(
            {
                'res': {
                    'tag': tag,
                    'tweet_id': id_primeiro_tweet,
                    'tweet_text': corpo_do_tweet,
                    'analise': analise
                }
            }
        )
    except:
        return jsonify({'res': 'Houve um erro. Tente novamente mais tarde.'})
