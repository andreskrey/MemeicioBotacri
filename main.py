#!/usr/bin/python3

from peewee import *
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
    mysql_username = os.environ.get['MYSQL_USERNAME']
    mysql_password = os.environ.get['MYSQL_PASSWORD']
else:
    credentials = open('credentials.json')
    credentials = json.load(credentials)
    client_id = credentials['CLIENT_ID']
    client_secret = credentials['CLIENT_SECRET']
    username = credentials['USERNAME']
    password = credentials['PASSWORD']
    mysql_username = credentials['MYSQL_USERNAME']
    mysql_password = credentials['MYSQL_PASSWORD']

# Connect database
db = MySQLDatabase('memes',
                   user=mysql_username,
                   passwd=mysql_password,
                   host='localhost')


class Memes(Model):
    thing_id = CharField()
    string = CharField()

    class Meta:
        database = db


db.connect()

# Connect to reddit
reddit = praw.Reddit(user_agent='MemeicioBotacri',
                     client_id=client_id, client_secret=client_secret,
                     username=username, password=password)

# Get comments
subreddit = reddit.subreddit('empleadoEstatalBot')
comments = subreddit.comments()

count = 0

# Loop over comments
for comment in comments:
    string = comment.body
    # Loop over results
    for memes in re.finditer('(\w+CIO\\b) (\w+CRI\\b)', string, re.IGNORECASE):
        meme = memes.group(0)

        # Filter Mauricio Macri (since it isn't dank enough)
        if meme.lower() != 'mauricio macri':

            # Check if we already are dank enough
            query = Memes.select().where(Memes.string == meme)
            if not query.exists():
                Memes(thing_id=comment.fullname, string=meme).save()
                comment.reply(
                    'Gracias, su colaboracion ha sido agregada a la lista de Memeicios Ⓡ \n## {} \n - - - - - \n Lista completa de Memeicios \n - - - - - \n ^(Soy un bot, *priip*) ^/ ^[Autor](/u/subtepass) ^/ [^Código ^fuente](https://github.com/andreskrey/MemeicioBotacri)'.format(
                        meme)
                )
                count += 1

print('Done, saved {} memes'.format(count))
