"""
Author:                 Nathan Dunne (with attributions)
Date last modified:     16/11/2018
Purpose:                Authenticate with twitter, fetch and clean tweets.
"""

import tweepy  # The tweepy library is the library used to fetch the twitter observations.
# MIT License Copyright (c) 2013-2014 Joshua Roesslein

import re  # Pythons regular expression library is used to clean up the observations.
import json  # Required for reading in credentials from a json file.


class TwitterInterface:
    api = ""

    # Twitter API credentials
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    def __init__(self):

        self.setCredentials()  # Set the credentials for authentications.
        self.api = self.authenticate()  # Authenticate using the set credentials.

    def setCredentials(self):
        """
        Retrieve credentials from json file and set for authentication.If this program was to be publicly available,
        hard-coding the credentials into source code would be a bad idea so they are stored in a git-ignored file.
        Advice and code used in part and modified from:
            chrisalbon.com/python/basics/store_api_credentials_for_open_source_projects/
        Copyright © Chris Albon, 2018
        """

        #  Load the json file that holds the credentials.
        with open('credentials.json') as creds:
            credentials = json.load(creds)

        # Set the credentials associated with the key value.
        self.consumer_key = credentials['consumer_key']
        self.consumer_secret = credentials['consumer_secret']
        self.access_key = credentials['access_token']
        self.access_secret = credentials['access_secret']

    def authenticate(self):
        """
        Authenticate with twitter using the authentication keys.
        """

        # Using the consumer key and consumer secret, create an authentication variable from twitters OAuth.
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # Using the authenticated keys, set the access token and secret.
        auth.set_access_token(self.access_key, self.access_secret)

        # Set rate limit variables to True to notify when waiting and prevent rate limit errors from occurring.
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        return api

    def fetchTweets(self, search_term, amount_of_tweets, exclude_retweets):
        """
        Fetch an amount of tweets based on a search term, possibly excluding retweets.
        Clean tweets up and add observations as dictionaries to a list, tweet_observations.
         """

        tweet_observations = []  # List to hold observation dictionaries.

        # As retweets are simply copies of already made tweets, they can be excluded by appending the search term.
        if exclude_retweets:
            search_term += ' -filter:retweets'

        print("Searching for tweets containing: " + search_term)
        print("\nFetching " + str(amount_of_tweets) + " twitter observations...")

        # For each tweet_observation in our search in English, up to an amount of tweets, based on a term.
        # tweet_mode='extended' is vital here as without it any tweet >140 characters will be cut when fetched.
        for tweet_observation in tweepy.Cursor(self.api.search,
                                               q=search_term,
                                               tweet_mode='extended',
                                               include_entities=True, lang="en").items(amount_of_tweets):

            """
            To avoid entering None(null) values into fields where no data can be found, selection structures are
            in place to determine if a value is null or not where null values have been previously observed.
            """
            if tweet_observation.place is None:
                tweet_observation.place = "noPlaceData"  # Define location as having no data.
            else:  # Retrieve location from the string.
                tweet_observation.place = self.retrieveLocation(str(tweet_observation.place))

            if tweet_observation.coordinates is None:
                tweet_observation.coordinates = "noCoordinatesData"  # Define coordinates as having no data.
            else:  # Retrieve coordinates from the string.
                tweet_observation.coordinates = self.retrieveCoords(str(tweet_observation.coordinates))

            if tweet_observation.in_reply_to_user_id is None:
                tweet_observation.in_reply_to_user_id = "noInReplyToUseridData"  # Define no data.

            if tweet_observation.in_reply_to_status_id is None:
                tweet_observation.in_reply_to_status_id = "noInReplyToStatusidData"  # Define no data.

            # Convert the text object to a string, encode it in utf-8.
            # '[1:]' strips out the 1st character of the string, removing the 'b' character that all tweets start with.
            tweet_observation.full_text = str(tweet_observation.full_text.encode("utf-8"))[1:]

            # Clean up the tweet text to remove unwanted text such as links and special characters.
            # This is required for much accurate sentiment analysis performed later.
            tweet_observation.full_text = self.clean_tweet_text(tweet_observation.full_text)

            # Add the relevant data to the tweet_observations using a dictionary structure.
            tweet_observations.append({'created_at': str(tweet_observation.created_at),
                                       'text': tweet_observation.full_text,
                                       'favorite_count': int(tweet_observation.favorite_count),
                                       'retweet_count': int(tweet_observation.retweet_count),
                                       'tweet_id': str(tweet_observation.id),
                                       'self_favorited': tweet_observation.favorited,
                                       'self_retweeted': tweet_observation.retweeted,
                                       'lang': tweet_observation.lang,
                                       'place': tweet_observation.place,
                                       'coordinates': tweet_observation.coordinates,
                                       'in_reply_to_user_id': tweet_observation.in_reply_to_user_id,
                                       'in_reply_to_status_id': tweet_observation.in_reply_to_status_id})

        print("Fetched " + str(amount_of_tweets) + " observations.")

        return tweet_observations

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def clean_tweet_text(tweet):
        """
        Utility function to clean the text in a tweet by removing links and special characters using regular expression.
        Code taken in part and modified from:
            https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-
        Copyright (c) 2018 Rodolfo Ferro
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # Hacks begin.

    """
    These retrieveLocation() and  retrieveCoords() (below) methods are string manipulation hacks to get the location and
    coordinate data if geo data is turned on by the user. I couldn't find any documentation or code for tweepy to
    extract the values from the place object so I had to write these somewhat questionable implementations.
    """

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def retrieveLocation(locString):

        try:
            list_of_values = str(locString).split(",")  # Split the string by a ",".
            unformatted_word = list_of_values[5]  # The full_name value of place is at the 6th index.
            formatted_word = unformatted_word[12:]  # Strip "full_name='" (first 12 letters) from full_name value.
        except:
            print("Error stripping down Place object data to location")
            return "placeDataInvalid"

        return formatted_word # Example returned data: California.

    @staticmethod  # Method is static as it alters no values of the self object.
    def retrieveCoords(coordsString):
        try:
            formatted_word = coordsString[33:-1]  # Strip the first 33 characters and last character from the string.
        except:
            print("Error stripping down Place object data to location")
            return "coordDataInvalid"

        return formatted_word  # Example returned data: [-86.4716, 40.0521].

    # Hacks end.
