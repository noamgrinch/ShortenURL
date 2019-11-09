from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import short_url
import sqlite3


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URL.db'
server.config['SQLALCHEMY_BINDS'] = { 'RR': 'sqlite:///Redirections.db'}
DB = SQLAlchemy(server)


class URLs(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    CreateDate = DB.Column(DB.DateTime, default=datetime.utcnow)
    LongURL = DB.Column(DB.String(150),nullable=False)
    shortURL = DB.Column(DB.String(150)) #Might be an error on generate, that's why it's not nullable=false.
    redirections = DB.Column(DB.Integer, default=0)

    def __repr__(self):
        return '<URLs %u>' % self.id

class Redirects(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    CreateDate = DB.Column(DB.DateTime, default=datetime.utcnow)
    LongURL = DB.Column(DB.String(150), nullable=False)
    shortURL = DB.Column(DB.String(150))

    def __repr__(self):
        return '<Redirects %r>' % self.id

#in line 35 we are adding 1 to the ID because of the first entry. We encode the URL before it enters the DB.

@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        longUrl = request.form['URLinput']
        try:
            latest = URLs.query.order_by(URLs.CreateDate).all()
            if not latest:
                latestID = 1
                newURL = URLs(LongURL=longUrl, shortURL=short_url.encode_url(latestID))
            else:
                latestID = latest[len(latest)-1].id
                newURL = URLs(LongURL=longUrl, shortURL=short_url.encode_url(latestID+1))
            DB.session.add(newURL)
            DB.session.commit()
            topost = []
            topost.append(newURL)
            return render_template('result.html', URLS=topost)
        except Exception as e: print(e)

    else:
       #URLS = URLs.query.order_by(URLs.CreateDate).all()
        return render_template('index.html')

def getRedStats():


    result = DB.engine.execute("SELECT COUNT(Id),strftime ('%D',CreateDate) hour FROM Redirects GROUP BY strftime ('%D',CreateDate)")

    for r in result:
        print (r[0])
        perDay = r[0]
        break;

    result = DB.engine.execute("SELECT COUNT(Id),strftime ('%H',CreateDate) hour FROM Redirects GROUP BY strftime ('%H',CreateDate)")

    for r in result:
        print (r[0])
        perHour= r[0]
        break;

    result = DB.engine.execute("SELECT IFNULL(COUNT(Id),0),strftime ('%M',CreateDate) hour FROM Redirects GROUP BY strftime ('%M',CreateDate) ORDER BY 2 DESC")

    for r in result:
        print (r[0])
        perMinute= r[0]
        break;

    redirectList = Redirects.query.all()
    return (len(redirectList))


def getAmountLinks():

    getLinks = URLs.query.all()
    return len(getLinks)


@server.route('/stats')
def showStats():

    amount = getAmountLinks()
    redirectStats = getRedStats()

    return render_template("stats.html", amount=amount,redirects = redirectStats)

@server.route('/<short>')
def redirectURL(short):
    newLink = URLs.query.filter_by(shortURL=short).first_or_404()

    newLink.redirections = newLink.redirections + 1
    newRed = Redirects(LongURL=newLink.LongURL, shortURL=newLink.shortURL)
    DB.session.add(newRed)
    DB.session.commit()

    return redirect('https://' + newLink.LongURL)

@server.errorhandler(400)
def badrequest(e):
    return "Error 400: Bad request."


@server.errorhandler(404)
def notfound(e):
    return "Error 404: Page was not found."

if __name__ == "__main__":
    server.run(debug=True)
