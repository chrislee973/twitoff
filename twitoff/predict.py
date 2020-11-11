"""Prediction of users based on tweet embeddings."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet
import spacy

model = spacy.load('model')

def predict_user(user1, user2, tweet_text):
    """Determine and return which user is more liekly to say a given Tweet."""

    user1 = User.query.filter(User.name == user1).one()
    user2 = User.query.filter(User.name == user2).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)), 
                            np.zeros(len(user2.tweets))])
    
    log_reg = LogisticRegression().fit(embeddings, labels)

    tweet_embedding = vectorize_tweet(tweet_text)
    return log_reg.predict(np.array(tweet_embedding).reshape(1,-1))


