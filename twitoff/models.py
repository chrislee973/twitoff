"""SQLAlchemy models and utility functions for Twitoff Application"""

from flask_sqlalchemy import SQLAlchemy



DB = SQLAlchemy()

class User(DB.Model):
    """Twitter User Table that will correspond to tweets - SQLAlchemy syntax"""
    id = DB.Column(DB.BigInteger, primary_key =True) # id column (primary key)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f"<User: {self.name}>"


class Tweet(DB.Model):
    """Tweet text data - associated with Users Table"""
    id = DB.Column(DB.BigInteger, primary_key = True)
    text = DB.Column(DB.Unicode(380))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable = False)
    user = DB.relationship('User', backref = DB.backref('tweets', lazy=True))

    def __repr__(self):
        return self.text


def insert_example_users():
    nick = User(id=1, name="Nick")
    elon = User(id=2, name="Elon")
    nick_tweet = Tweet(id=1, text= "Hi I'm Nick!", user = nick)
    elon_tweet = Tweet(id=2, text = "Ha. Cybertruck big and go vroom.", user = elon)
    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.commit()

