"""
Author:                 Nathan Dunne
Date last modified:     16/11/2018
Purpose:                Fetch twitter data based on a search term, generate CSV and JSON files to store data, display
                        sentiment analysis and selected+formatted data frame as per assignment as a table.
Convention:             This program adheres to the PEP8 Python programming convention throughout.
"""
#!/usr/bin/python

# Local file imports.
import TwitterInterface  # The local class used for fetching and cleaning tweets.
import FileGenerator  # The local class used for generating CSV and JSON files.
import DataFrameDisplayFormat  # The local class used for making, formatting and displaying data frames.
import SentimentAnalysis  # The local class used for sentiment analysis.
import sys  # Required for accessing parameters passed in from a console.


def main():
    """
    main() handles the preset and passed in parameters, calls the core functions of getting data, making files and
    displaying the information pertaining to the data. Parameters: string(search_term), int(amount_of_observations),
    boolean(exclude_retweets)
    """
    arguments = sys.argv[1:]  # The arguments are at the first position in the argument vector.
    argument_amt = len(arguments)  # Knowing the amount of arguments helps to check if the input is valid.

    # Preset parameters.
    search_term = "Automation"
    amount_of_observations = 500
    exclude_retweets = True  # Can set to false to include retweets.

    # If arguments are passed in and if there is not the correct amount of arguments.
    if argument_amt > 0 and argument_amt != 3:
        print("Invalid argument amount, using preset parameters.")
    elif argument_amt > 0:  # If we have arguments, use them as parameters when fetching tweets.
        try:
            search_term = str(sys.argv[1])
            amount_of_observations = int(sys.argv[2])
            exclude_retweets = bool(int(sys.argv[3]))
        except ValueError:  # Catch invalid values.
            print("Value Error, using preset parameters.")
            search_term = "Automation"
            amount_of_observations = 500
            exclude_retweets = True

    # Generate a data set based on a search term, amount of tweets and with the option of excluding retweets.
    twitter_data_set = generateDataSet(search_term, amount_of_observations, exclude_retweets)

    # Generate a CSV and JSON file based on the acquired data set.
    generateFiles(twitter_data_set, search_term)

    # The assignment calls for the top 10 favourited tweets, this value dictates how many to print out from the head.
    row_amount_from_head = 10

    # Display the required data in line with the assignment.
    displayAssignmentData(twitter_data_set, row_amount_from_head)


def setPresets():
    search_term = "Automation"
    amount_of_observations = 500
    exclude_retweets = True


def generateDataSet(search_term, amount_of_observations, exclude_retweets):
    """
    generateDataSet() will use the parameters to retrieve tweet observations from twitter and store them in a list of
    dictionaries to return.
    """

    twitter_interface = TwitterInterface.TwitterInterface()  # Instantiate TwitterInterface object.

    # Fetch an amount of twitter observations based on a search term, possibly excluding retweets.
    twitter_data_set = twitter_interface.fetchTweets(search_term, amount_of_observations, exclude_retweets)

    return twitter_data_set


def generateFiles(data_set, search_term):
    """
    generateFiles() uses the data_set from generateDataSet() to create CSV and JSON files, named with the search term.
    """

    file_generator = FileGenerator.FileGenerator()  # Instantiate FileGenerator object.

    csv_file_name = search_term + "twitterDataCSV"  # Name the csv file.
    json_file_name = search_term + "twitterDataJSON"  # Name the json file.

    file_generator.createCSV(data_set, csv_file_name)  # Create csv file with the given data set and filename.
    file_generator.createJSON(data_set, json_file_name)  # Create json file with the given data set and filename.


def displayAssignmentData(twitter_data_set, row_amount):
    """
    displayAssignmentData() uses the data_set from generateDataSet() to create a data frame which can then be
    formatted and sorted. The data frame is then analysed for sentiment and the results are displayed. Finally, the data
    frame is used with tabulate to format and display an orderly table.
    """
    data_display_format = DataFrameDisplayFormat.DataFrameDisplayFormat()  # Instantiate FileGenerator object.

    # Convert the data set to a data frame.
    twitter_data_frame = data_display_format.convertDataSetToDataFrame(twitter_data_set)

    # Format the frame, sorting columns and rows.
    twitter_data_frame = data_display_format.formatDataFrame(twitter_data_frame)

    sentiment_analysis = SentimentAnalysis.SentimentAnalysis()  # Instantiate SentimentAnalysis object.

    sentiment_analysis.displaySentimentPercentages(twitter_data_frame)  # Display sentiment analysis results.

    show_index = True  # Set to show index numbers.
    # Display formatted data frame using an amount of rows.
    data_display_format.displayDataFrame(twitter_data_frame, row_amount, show_index)


if __name__ == "__main__":
    main()
