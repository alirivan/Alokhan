from flask import render_template, request, redirect
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import desc
from transformers import pipeline


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Alik1234@localhost/final'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.String(255))
    password = db.Column( db.String(1000))


    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
    def __repr__(self):
        return '<Users %r>' % self.id

class Tablecoin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_coin = db.Column( db.String(255))
    news = db.Column( db.String(7000))


    def __init__(self,name_of_coin, news):
        self.name_of_coin = name_of_coin
        self.news = news
    def __repr__(self):
        return '<Tablecoin %r>' % self.id



app.config['SECRET_KEY'] = 'SECRET'



@app.route('/login')
def login():
    auth = request.authorization

    user = Users.query.filter_by(name=auth.username).first()

    if user.password == auth.password:
        return redirect('/webpage')



@app.route('/webpage')
def webpage():
    return render_template('index.html')


@app.route('/coin', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        names = request.form['name']
        url = 'https://coinmarketcap.com/currencies{0}'.format(names)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        allNews = soup.findAll('p')
        strr=str(allNews)
        new_ex = Tablecoin(name_of_coin=names, news=strr)
        try:
            db.session.add(new_ex)
            db.session.commit()
            return redirect('/coin')
        except:
            return 'Something wrong'


    else:
        tablecoin = Tablecoin.query.order_by(desc(Tablecoin.id)).first()#to find url and name of coin
        url = 'https://coinmarketcap.com/ru/currencies/{0}'.format(tablecoin.name_of_coin)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        summarizer = pipeline("summarization")
        allNews = soup.findAll('p')
        return render_template('index.html', allNews=allNews, summarizer = summarizer )


if __name__ == '__main__':
    app.run(debug=True)
