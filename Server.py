from flask import Flask, render_template, request, redirect
import short_url
from DB import DB
from Models import URLs, Redirects, BadRequests

############################################### DB configuration ###############################################
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URL.db'
server.config['SQLALCHEMY_BINDS'] = { 'RR': 'sqlite:///Redirections.db' , 'BR' : 'sqlite:///BadRequests.db'} # RR = Redirections , BR = BadRequests
DB.init_app(server)


with server.app_context():
    DB.create_all()
############################################### DB configuration  ###############################################



#in line 31 we are adding 1 to the ID because of the first entry. We encode the URL before it enters the DB.


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
            return render_template('index.html', URLS=topost)
        except Exception as e: print(e)

    else:
        return render_template('index.html')


############################################### Routes ###############################################

@server.route('/stats')
def showStats():

    amount = getAmountLinks()
    redirectStats = getRedStats()
    badrequests = getBadRequests()

    return render_template("stats.html", amount=amount,redirectsDay = redirectStats[0],redirectsHour = redirectStats[1],redirectsMinute = redirectStats[2],errorsDay=badrequests[0],errorsHour=badrequests[1],errorsMinute=badrequests[2])

@server.route('/<short>')
def redirectURL(short):
    newLink = URLs.query.filter_by(shortURL=short).first_or_404()

    newLink.redirections = newLink.redirections + 1
    newRed = Redirects(LongURL=newLink.LongURL, shortURL=newLink.shortURL)
    DB.session.add(newRed)
    DB.session.commit()

    return redirect('https://' + newLink.LongURL)


############################################### Routes ###############################################



############################################### Stats functions ###############################################


def getRedStats():


    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM Redirects WHERE CreateDate > datetime('now', '-24 hours')")

    for r in result:
        perDay = r[0]
        break;

    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM Redirects WHERE CreateDate > datetime('now', '-1 hours')")

    for r in result:
        perHour= r[0]
        break;

    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM Redirects WHERE CreateDate > datetime('now', '-1 minutes')")

    for r in result:
        perMinute= r[0]
        break;

    redirectList = [perDay, perHour, perMinute]

    return redirectList


def getAmountLinks():

    getLinks = URLs.query.all()
    return len(getLinks)


def getBadRequests():

    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM BadR WHERE CreateDate > datetime('now', '-24 hours')")

    for r in result:
        perDay = r[0]
        break;

    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM BadR WHERE CreateDate > datetime('now', '-1 hours')")

    for r in result:
        perHour= r[0]
        break;

    result = DB.engine.execute("SELECT COUNT(Id) as 'count' FROM BadR WHERE CreateDate > datetime('now', '-1 minutes')")

    for r in result:
        perMinute= r[0]
        break;

    errorsList = [perDay, perHour, perMinute]

    return errorsList
############################################### Stats functions ###############################################


############################################### Error Handlers ###############################################
@server.errorhandler(400)
def badrequest(e):

    newBadReq = BadRequests()
    DB.session.add(newBadReq)
    DB.session.commit()

    return "Error 400: Bad request."


@server.errorhandler(404)
def notfound(e):
    return "Error 404: Page was not found."

############################################### Error Handlers ##############################################

