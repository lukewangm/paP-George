# Group 20
CSCI401 / Fall 2024

## Stetup
### Setting up environment
1. Install Python 3.8 or later
2. Install the required packages with `pip install -r requirements.txt`

### Downloading the database
Prepare the dataset by going into the "scraper" folder with command `cd scraper` and running  `python scraper.py --journal "Medical Case Reports"`. This will download a articles.sqlite file containing a database of medical documents. 

### Setup OpenAI API
At the root directory, create a file called `credentials.py` and add the OpenAI API key as a variable called `OPENAI_API_KEY`. See group chat for more information. 