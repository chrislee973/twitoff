"""Retrieve Tweets, embeddings, and persist in the database."""
from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']


TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

model = spacy.load('model')


def vectorize_tweet(tweet_text):
    return model(tweet_text).vector

def add_or_update_user(username):
    """Add or update a user and their tweets, error if not Twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or 
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        
        #Let's get the tweets - focusing on primary(not retweet/reply)
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, 
                  tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f'Error processing {username}: {e}')
        raise e
    else: 
        DB.session.commit()


def insert_example_users():
    # nick = User(id=1, name="Nick")
    # elon = User(id=2, name="Elon")
    # nick_tweet = Tweet(id=1, text= "Hi I'm Nick!", user = nick)
    # elon_tweet = Tweet(id=2, text = "Ha. Cybertruck big and go vroom.", user = elon)
    # DB.session.add(nick)
    # DB.session.add(elon)
    # DB.session.commit()
    add_or_update_user('austen')
    add_or_update_user('elonmusk')
