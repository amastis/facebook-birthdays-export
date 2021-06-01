"""facebook_birthdays.py
Usage:
  facebook_birthdays.py -f <file>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file <file>          File to import (har file)
"""
from haralyzer import HarParser, HarPage
from bs4 import BeautifulSoup
from json import loads
import pandas as pd
from pathlib import Path
from sys import exit
import docopt


# goes through the birthday data to grab the name, month, day of your friends birthday
def json_birthday(friend_data):
	friend_month = friend_data['viewer']['all_friends_by_birthday_month']['edges']
	birthdays = []
	for item in friend_month:
		month = item['node']['month_name_in_iso8601']
		for elm in item['node']['friends']['edges']:
			url = elm['node']['url']
			name = elm['node']['name']
			day = elm['node']['birthdate']['day'] # birthdate = year, day, month
			year = elm['node']['birthdate']['year']
			birthdays.append({'url': url, 'name': name, 'month': month, 'day': day, 'year': year})
	return birthdays


if __name__ == "__main__":
	args =  docopt.docopt(__doc__, version="1.0")
	in_file = args["--file"]
	if 'har' not in in_file.split('.')[-1]:
		print("Please use a file with a '.har' extension")
		exit(-1)

	birthday_data = []
	with open(in_file, 'r') as f:
		har_parser = HarParser(loads(f.read()))
		data = har_parser.har_data
		# check if ['content']['mimeType'] == 'text/html' or 'json'
		html_data = data['entries'][0]['response']['content']['text'] 
		soup = BeautifulSoup(html_data, 'html.parser')
		find_elm = soup.find_all('script')

		for elm in find_elm: # first element is inside html data - can convert to json
			if elm.string and 'birthdate' in elm.string:
				beginining_text = 'ScheduledApplyEach,' # json starts with {"require"
				find_text_index = len(beginining_text) + elm.string.find(beginining_text)
				last_index = elm.string.rfind(');});});') # get rid of ';'s
				json_data = loads(elm.string[find_text_index:last_index])
				# cycle through 'today', 'recent', 'upcoming', 'viewer'
				friend_data = json_data['require'][3][3][1]['__bbox']['result']['data']
				birthday_data += json_birthday(friend_data)

		for elm in data['entries'][1:]: # rest of entries are in json style
			if 'text' in elm['response']['content']['mimeType']:
				json_data = elm['response']['content']['text']
				if 'birthdate' in json_data:
					temp = loads(json_data)
					birthday_data += json_birthday(temp['data'])

	# put data into a CSV file + download to downloads folder
	title = 'facebook_birthday_data.csv'
	facebook_df = pd.DataFrame(birthday_data)
	facebook_df.to_csv(str(Path.home() / "Downloads/") + '/' + title, index=False)
	print('downloaded', title)
