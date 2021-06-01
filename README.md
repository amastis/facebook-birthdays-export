# Facebook Birthdays Export
To easily export your friends' birthdays to CSV format, all you need to do is download the har file from: https://www.facebook.com/events/birthdays

Requires Python 3.6+

## Tutorial on downloading har files 
Here is a link for an explanation on how to download har files from your browser of choice:

https://knowledge.vidyard.com/hc/en-us/articles/360009996213-Download-a-HAR-file-from-your-browser


## Installing
```bash
$ pip3 install -r requirements.txt
```

## Help Menu

```bash
Usage:
  facebook_birthdays.py -f <file>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file <file>          File to import (har file)
```

## Sample Output

```bash
$ python3 facebook_birthdays.py --file facebook_birthday.har
downloaded facebook_birthday_data.csv
```
