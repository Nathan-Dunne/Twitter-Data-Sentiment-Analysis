Requirements:
	cmd run:
		pip install textblob pandas tabulate tweepy
	Python 3.3 or greater.

Included files:
	README.txt
	main.py
	TwitterInterface.py
	DataDisplayFormat.py
	FileGenerator.py
	SentimentAnalysis.py
	credentials.json
	Sentiment Analysis Research and Implementation.docx
	README.txt


Usage:
    	Edit the "credentials.json" file to use your personal credentials for the twitter API.
	This program is best used with an advanced console. Recommendation: Pycharm IDE console.
	While it can be run on the command line it will not look as intended due to the
	inability of the windows command line or powershell to scroll horizontally.

Note:

If using preset parameters (2000 observations) this file can only generally finish 
excuting once every 15 minutes due to rate limits imposed by the Twitter API.
Functionality is in place to allow continuation of execution after a period of time if rate limit is met.

main.py can be run as is or provided with arguments.
		Argument 1: Search Term e.g Pokemon.
		Argument 2: Amount of twitter observations to fetch. e.g 1500.
		Argument 3. Exclude retweets or not, numeric to boolean. i.e 1 for TRUE, 0 for FALSE.

If no arguments are provided the program will use preset parameters. 
   		# Preset parameters.
    		search_term = "Automation"
    		amount_of_observations = 500
    		exclude_retweets = True 

Full example from cmd:
		python main.py
		python main.py "Automation" 500 1
