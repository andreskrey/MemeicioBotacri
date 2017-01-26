import praw
import re
import os
import json

# Get and set credentials
if os.environ.get('CURRENT_ENV') == 'HEROKU':
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
else:
    credentials = open('credentials.json')
    credentials = json.load(credentials)
    client_id = credentials['CLIENT_ID']
    client_secret = credentials['CLIENT_SECRET']
    username = credentials['USERNAME']
    password = credentials['PASSWORD']

# Connect to reddit
reddit = praw.Reddit(user_agent='MemeicioBotacri',
                     client_id=client_id, client_secret=client_secret,
                     username=username, password=password)

# Get comments
subreddit = reddit.subreddit('empleadoEstatalBot')
comments = subreddit.comments()

# Loop over comments
for comment in comments:
    string = comment.body
    # Loop over results
    for meme in re.finditer('(\w+CIO\\b) (\w+CRI\\b)', string, re.IGNORECASE):
        test=meme.group(0)
