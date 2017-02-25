#!/usr/bin/env python

from gutenberg import read_book, parse_sentences
import re
import twitter
import config

def sentence_to_tweets(sentence):
    tweets = []
    if len(sentence) <= 140:
        tweets.append(sentence)
    else:
        words = sentence.split()
        i = 0
        while i <= len(words):
            tweet = ''
            j = 0
            while len(tweet) < 120 and j <= len(words):
                tweet = ' '.join(words[i:j])
                j += 1
            tweets.append(tweet)
            i += j
    return tweets      

def tweet(api, tweets):
    status = api.PostUpdate(tweets.pop(0))
    if len(tweets) > 0:
        for tweet in tweets:
            api.PostUpdate(tweet, in_reply_to_status_id=status.id)

def main():
    # Authenticate to Twitter
    api = twitter.Api(consumer_key        = config.consumer_key,
                      consumer_secret     = config.consumer_secret,
                      access_token_key    = config.access_token_key,
                      access_token_secret = config.access_token_secret)

    # Get last status so we can determine our position in the book
    statuses = api.GetUserTimeline(screen_name=config.screen_name, count=1)
    result = re.search('\[([0-9]+)\]$', statuses[0].text)
    position = int(result.group(1))

    # Get the book and break into sentences
    #book = get_book(config.book_url)
    book = read_book(config.book_file)
    sentences = parse_sentences(config.title, book)

    # Format the sentences into tweets and post
    sentence = '{0} [{1}]'.format(sentences[position], position + 1)
    tweets = sentence_to_tweets(sentence)
    tweet(api, tweets)
    return sentence
