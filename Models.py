from datetime import datetime
from DB import DB




############################################### Tables configuration ###############################################
class URLs(DB.Model):
    __tablename__ = 'URLs'
    id = DB.Column(DB.Integer, primary_key=True)
    CreateDate = DB.Column(DB.DateTime, default=datetime.utcnow)
    LongURL = DB.Column(DB.String(150),nullable=False)
    shortURL = DB.Column(DB.String(150)) #Might be an error on generate, that's why it's not nullable=false.
    redirections = DB.Column(DB.Integer, default=0)

    def __repr__(self):
        return '<URLs %u>' % self.id

class Redirects(DB.Model):
    __tablename__ = 'Redirects'
    id = DB.Column(DB.Integer, primary_key=True)
    CreateDate = DB.Column(DB.DateTime, default=datetime.utcnow)
    LongURL = DB.Column(DB.String(150), nullable=False)
    shortURL = DB.Column(DB.String(150))

    def __repr__(self):
        return '<Redirects %r>' % self.id


class BadRequests(DB.Model):
    __tablename__ = 'BadR'
    id = DB.Column(DB.Integer, primary_key=True)
    CreateDate = DB.Column(DB.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<BadR %b>' % self.id

############################################### Tables configuration ###############################################