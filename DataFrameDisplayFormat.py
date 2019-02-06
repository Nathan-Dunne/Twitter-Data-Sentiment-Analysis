"""
Author:                 Nathan Dunne
Date last modified:     16/11/2018
Purpose:                Create a data frame from a data set, format and sort said data frame and display
                        data frame as a table.
"""

import pandas  # The pandas library is used to create, format and sort a data frame.
# BSD 3-Clause License
# Copyright (c) 2008-2012, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development

from tabulate import tabulate  # The tabulate library is used to better display the pandas data frame as a table.
# MIT License Copyright (c) 2018 Sergey Astanin


class DataFrameDisplayFormat:
    def __init__(self):
        pass  # There is nothing to initialise so pass is called here. The pass statement is a null operation.

    @staticmethod  # Method is static as it alters no values of the self object.
    def convertDataSetToDataFrame(data_set):
        """
        Convert a data set to a pandas data frame.
        """

        data_frame = pandas.DataFrame(data_set)  # Convert the data set (List of dictionaries) to a pandas data frame.

        return data_frame

    @staticmethod  # Method is static as it alters no values of the self object.
    def formatDataFrame(data_frame):
        """
        Format and sort a data frame.
        """

        data_frame = data_frame[['favorite_count',  # Order and display only these three columns.
                                 'retweet_count',
                                 'text',
                                 ]]

        print("\nSorting data by 'favorite_count', 'retweet_count', descending.")

        # Sort the rows first by favorite count and then by retweet count in descending order.
        data_frame = data_frame.sort_values(by=['favorite_count', 'retweet_count'], ascending=False)

        return data_frame

    @staticmethod  # Method is static as it neither accesses nor alters any values or behaviour of the self object.
    def displayDataFrame(data_frame, amount_of_rows, show_index):
        """
        Display a data frame in table format using tabulate.
        """

        # Print out an amount of rows from the data frame, possibly with showing the index, with the headers as the
        # data frame headers using the table format of PostgreSQL.
        # Tabulate can't display the word "Index" in the index column so it is printed out right before the table.
        print("\nIndex")
        print(tabulate(data_frame.head(amount_of_rows),
                       showindex=show_index,
                       headers=data_frame.columns,
                       tablefmt="psql"))
