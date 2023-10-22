import os
import tweepy
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def run_twitter_etl():
    # Twitter Authentication
    auth = tweepy.OAuthHandler(os.environ.get(
        'API_KEY_'), os.environ.get('API_SECRET_KEY'))
    auth.set_access_token(os.environ.get('ACCESS_KEY'),
                          os.environ.get('ACCESS_SECRET_KEY'))

    # Creating an API object
    api = tweepy.API(auth)

    # tweets = api.user_timeline(screen_name="@elonmusk",
    #                            count=200, include_rts=False, tweet_mode='extended')

    # # print(tweets)
    try:
        tweets = api.user_timeline(screen_name="@elonmusk", count=10)
        tweets_list = []
        for tweet in tweets:
            text = tweet._json()

            refined_tweet = {"user": tweet.user.screen_name,
                             'text': text,
                             'favorite_count': tweet.favorite_count,
                             'retweet_count': tweet.retweet_count,
                             'created_at': tweet.created_at}

            tweets_list.append(refined_tweet)

        df = pd.DataFrame(tweets_list)
        df.to_csv('refined_tweets.csv')

    except tweepy.errors.Unauthorized as e:
        print(f"Twitter API Unauthorized Error: {e.response.text}")
