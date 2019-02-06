"""
Author:                 Nathan Dunne (with attributions)
Date last modified:     16/11/2018
Purpose:                Analyse the sentiment of tweets and display the sentiment analysis of those tweets.
"""

from textblob import TextBlob  # Textblob is a natural language processing library that has a sentiment analysis module.
# Copyright 2013-2018 Steven Loria


class SentimentAnalysis:

    def __init__(self):
        pass

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def analyseSentiment(tweet):
        """
        Utility function to classify the polarity of a tweet using Textblob.
        Code used in part and modified from:
            https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-
        Copyright (c) 2018 Rodolfo Ferro
        """
        analysis = TextBlob(tweet)  # Use TextBlob to return an analysis on a tweet text string.

        # If the polarity of the sentiment is positive it is determined to be a positive tweet
        if analysis.sentiment.polarity > 0:
            return 1
        # If the polarity of the sentiment is 0 it is determined to be a neutral tweet.
        elif analysis.sentiment.polarity == 0:
            return 0
        # If the polarity of the sentiment is negative it is determined to be a negative tweet.
        else:
            return -1

    def displaySentimentPercentages(self, data_frame):
        """
        Utility function to display the sentiment percentages from a set of tweets.
        Code used in part and modified from:
            https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-
        Copyright (c) 2018 Rodolfo Ferro
        """
        print("\nProcessing Sentiment Analysis")

        # For each tweet text component in given data frame, analyse and store the sentiment value.
        data = [self.analyseSentiment(tweet) for tweet in data_frame['text']]

        # Breakdown the polarities of all the tweets into 3 sub-lists.
        # Identify all the positive tweets.
        positive_tweets = [tweet for index, tweet in enumerate(data) if data[index] > 0]

        # Identify all the neutral tweets.
        neutral_tweets = [tweet for index, tweet in enumerate(data) if data[index] == 0]

        # Identify all the negative tweets.
        negative_tweets = [tweet for index, tweet in enumerate(data) if data[index] < 0]

        # The % of each perception is the size of each sub list in reference to the size of the whole data frame.
        print("Percentage of positive tweets: {}%".format(len(positive_tweets) * 100 / len(data)))
        print("Percentage of neutral tweets: {}%".format(len(neutral_tweets) * 100 / len(data)))
        print("Percentage of negative tweets: {}%".format(len(negative_tweets) * 100 / len(data)))
