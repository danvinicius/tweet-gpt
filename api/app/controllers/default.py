from flask import request, jsonify
from app import app, db

from app.services import ai_analysis
ai = ai_analysis.AI()

from app.services import social_media
media = social_media.SocialMedia()


import mysql.connector
import bcrypt

@app.route("/")
def root():
    return "<h1>Flask API</h1>"


@app.route("/usuarios", methods=["POST", "GET"])
def cadastro():
    if request.method == "POST" and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            senha_bytes = password.encode('utf-8')
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

            cursor = db.cursor()

            sql = "INSERT INTO User (name, email, senha) VALUES (%s, %s, %s)"
            val = (name, email, senha_hash)
            cursor.execute(sql, val)

            db.commit()
        except mysql.connector.Error as e:
            print(e)
            return "Erro! O cadastro não foi realizado."

        return "Cadastro realizado!"
            


@app.route("/usuarios/login", methods=["POST"])
def login():
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            
            cursor = db.cursor()
            cursor.execute("SELECT * FROM User WHERE email=%s", (email, ))
            resultado = cursor.fetchall()
            print(password.encode('utf-8'))
            print(resultado[0][2].encode('utf-8'))
            if not resultado:
                raise Exception("Usuário e/ou senha incorreto(a/s)")
            
            if not bcrypt.checkpw(password.encode('utf-8'), resultado[0][3].encode('utf-8')):
                raise Exception("Usuário e/ou senha incorreto(a/s)")

        except mysql.connector.Error as e:
            print(e)
            return "Erro! O Login não foi realizado."

        return "Login realizado!"

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
