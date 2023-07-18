from dotenv import load_dotenv

from flask_cors import cross_origin
load_dotenv()
from os import environ
from flask import request, jsonify
import flask
from app import app, db

from app.services import ai_analysis

ai = ai_analysis.AI()

from app.services import social_media

media = social_media.SocialMedia()

import mysql.connector
import bcrypt
import jwt

secret = environ['JWT_SECRET']


@app.route("/")
def root():
    return "<h1>Flask API</h1>"

@app.route("/usuarios", methods=["POST"])
@cross_origin()
def cadastro():
    if request.method == "POST":
        try:
            data = request.get_json(silent=False)
            nome = data["nome"]
            email = data["email"]
            senha = data["senha"]

            if type(email) != str or type(nome) != str or type(senha) != str:
                return jsonify({"error": "Informações inválidas"}), 400

            senha_bytes = senha.encode("utf-8")
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

            cursor = db.cursor()

            sql = "INSERT INTO User (nome, email, senha) VALUES (%s, %s, %s)"
            val = (nome, email, senha_hash)
            cursor.execute(sql, val)

            db.commit()

            encoded_jwt = jwt.encode({"email": email, "exp": 604800000 }, secret or 'secret', algorithm="HS256")

            return (
                jsonify(
                    {
                        "message": {"token": encoded_jwt},
                    }
                ),
                200,
            )
        except KeyError as e:
            print(e)
            return jsonify({"error": "Informações insuficientes"}), 400

        except mysql.connector.Error as e:
            print(e)
            return (
                jsonify(
                    {
                        "error": "Usuário já cadastrado. Faça login.",
                    }
                ),
                500,
            )

    return None

@app.route("/usuarios/login", methods=["POST"])
@cross_origin()
def login():
    if request.method == "POST":
        try:
            data = request.get_json(silent=False)
            email = data["email"]
            senha = data["senha"]

            if type(email) != str or type(senha) != str:
                return jsonify({"error": "Informações inválias"}), 400

            cursor = db.cursor()
            cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
            resultado = cursor.fetchall()
            if not resultado:
                return jsonify({"error": "Usuário não encontrado"}), 400

            if not bcrypt.checkpw(
                senha.encode("utf-8"), resultado[0][3].encode("utf-8")
            ):
                return jsonify({"error": "Senha incorreta"}), 400

            encoded_jwt = jwt.encode({"email": email, "exp": 604800000 }, secret or 'secret', algorithm="HS256")
            return jsonify({"message": {"token": encoded_jwt}}), 200

        except KeyError as e:
            print(e)
            return jsonify({"error": "Informações insuficientes"}), 400

        except mysql.connector.Error as e:
            print(e)
            return jsonify({"error": "Erro ao realizar cadastro. Tente novamente mais tarde."}), 500
    return None


# ex: http://localhost:5000/search?tag=brasil
@app.route("/search")
@cross_origin()
def search_tweet():
    try:
        headers = flask.request.headers
        bearer = headers.get("Authorization")
        
        if (bearer == None or len(bearer.split()) < 2):
            return jsonify({"error": "Usuario não autorizado"}), 400

        token = bearer.split()[1]
            
        decoded_token = jwt.decode(token, secret or 'secret', algorithms=["HS256"])
        
        email = decoded_token['email']
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
        resultado = cursor.fetchall()
        
        if not resultado:
            return jsonify({"error": "Usuario não autorizado"}), 400

        query = request.args.get("tag")
        tag = query

        tweet = media.fetch_from_twitter(tag)
        chatgpt_analysis = ai.analise_chat_gpt(tweet[1])

        return (
            jsonify(
                {
                    "message": {
                        "tag": tag,
                        "tweet_id": tweet[0],
                        "tweet_text": tweet[1],
                        "user": tweet[2],
                        "date": tweet[3],
                        "analysis": chatgpt_analysis,
                    }
                }
            ),
            200,
        )
    except (KeyError, jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError) as e:
        print(e)
        return jsonify({"error": "Usuario não autorizado"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Houve um erro. Tente novamente mais tarde."}), 500
