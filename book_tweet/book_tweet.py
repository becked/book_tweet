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
        tweet_word_count = 0
        i = 0
        j = 0
        while j <= len(words):
            tweet = ''
            j = i
            while len(tweet) < 120 and j <= len(words):
                tweet = ' '.join(words[i:j])
                j += 1
            tweets.append(tweet)
            i += (len(words[i:j])-1)
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

    # Get last status with a sentence ending so we can determine our position in the book
    for i in range(1,100):
        statuses = api.GetUserTimeline(screen_name=config.screen_name, count=i)
        result = re.search('\[([0-9]+)\]$', statuses[i-1].text)
        if result:
            position = int(result.group(1))
            break

    # Get the book and break into sentences
    book = read_book(config.book_file)
    sentences = parse_sentences(config.title, book)

    # Format the sentences into tweets and post
    sentence = '{0} [{1}]'.format(sentences[position], position + 1)
    tweets = sentence_to_tweets(sentence)
    tweet(api, tweets)
    return sentence
