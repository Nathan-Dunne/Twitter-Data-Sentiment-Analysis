"""
Author:                 Nathan Dunne
Date last modified:     16/11/2018
Purpose:                Generate a csv and json file from a data set.
"""

import csv  # Python has a built in csv library we can use to create a csv file
import json  # Python has a built in json library we can use to create a json file.


class FileGenerator:

    def __init__(self):
        pass  # There is nothing to initialise so pass is called here. The pass statement is a null operation.

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def createCSV(tweets, filename):
        print("\nCreating CSV file: " + filename)

        headers = tweets[0]  # Use an index of the list, which has the dictionary keys, as the headers.

        with open(filename+".csv", 'w', newline='') as csv_file:

            writer = csv.writer(csv_file)  # Instantiate the writer object.
            writer.writerow(headers)  # Write the first row using the headers.

            for each_tweet in tweets:  # For each dictionary object (tweet data) in the list (of tweet data sets)
                # Write the values of the dictionary object (tweet data) as a new row.
                writer.writerow(each_tweet.values())

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def createJSON(tweets, filename):
        print("Creating JSON file: " + filename)

        with open(filename+".json", 'w') as outfile:
            json.dump(tweets, outfile)
