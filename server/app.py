#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    datas=Article.query.all()
    articles=[]

    for data in datas:
        article={
            'id':data.id,
            'author':data.author,
            'title':data.title,
            'content':data.content,
            'preview':data.preview,
            'minutes_to_read':data.minutes_to_read,
            'date':data.date,
            'user_id':data.user_id
        }
        articles.append (article)
    
    return make_response(jsonify(articles),200)

@app.route('/articles/<int:id>')
def show_article(id):
    show_articles=Article.query.filter(Article.id == id).first()
    return handle_request(show_articles)
    
def handle_request(show_articles):
    if 'page_views' not in session:
       session['page_views'] =0

    session['page_views'] +=1

    if session['page_views'] <=3:
        response_body={
            'id':show_articles.id,
            'author':show_articles.author,
            'title':show_articles.title,
            'content':show_articles.content,
            'preview':show_articles.preview,
            'minutes_to_read':show_articles.minutes_to_read,
            'date':show_articles.date,
            'user_id':show_articles.user_id 
        }
        status=200
        return make_response(jsonify(response_body),status)
    
    else: 
        response_body={'message':'Maximum pageview limit reached'}
        status=401
        return make_response(jsonify(response_body),status)

if __name__ == '__main__':
    app.run(port=5555)
