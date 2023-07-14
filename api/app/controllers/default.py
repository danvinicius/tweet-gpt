from flask import request, jsonify
from app import app, db

from app.models.tables import User

from app.services import ai_analysis
ai = ai_analysis.AI()

from app.services import social_media
media = social_media.SocialMedia()


@app.route("/")
def root():
    return "<h1>Flask API</h1>"


@app.route("/usuarios", methods=["POST"])
def cadastro():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name and email and password:
            usuario = User(name, email, password)
            db.session.add(usuario)
            db.session.commit()


@app.route("/usuarios/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            usuario = User.query.filter_by(email=email).first()

            if usuario and usuario.check_password(password):
                return jsonify({'res': 'Login bem-sucedido!'})

    return jsonify({'res': 'Credenciais inválidas ou login falhou.'})

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
