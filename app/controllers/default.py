from flask import request, jsonify
from app import app

from app.services import ai_analysis
ai = ai_analysis.AI()

from app.services import social_media
media = social_media.SocialMedia()

# ex: http://localhost:5000/search?tag=brasil
@app.route('/search')
def search_tweet():
    try:
        query = request.args.get('tag')
        tag = '#' + query
        
        tweet = media.fetch_from_twitter(tag)
        chatgpt_analysis = ai.analise_chat_gpt(tweet[1])

        return jsonify(
            {
                'res': {
                    'tag': tag,
                    'tweet_id': tweet[0],
                    'tweet_text': tweet[1],
                    'analise': chatgpt_analysis
                }
            }
        )
    except:
        return jsonify({'res': 'Houve um erro. Tente novamente mais tarde.'})
