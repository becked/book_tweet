import nltk
import re
import requests

def read_book(file_name):
    book = open(file_name, 'r') 
    return book.read() 

def get_book(url):
    page = requests.get(url)
    return ' '.join(page.content.splitlines())

def find_beginning(title, book):
    m = re.search('{0}\s+CHAPTER'.format(title), book)
    if m:
        beginning = m.start()
    else:
        beginning = book.find('START OF THIS PROJECT GUTENBERG')
    return beginning

def find_ending(title, book):
    ending = book.rfind('APPENDIX')
    if ending == -1:
        ending = book.rfind('INDEX')
        if ending == -1:
            ending = book.rfind('End of the Project Gutenberg')
    return ending

def parse_sentences(title, book):
    beginning = find_beginning(title, book)
    ending = find_ending(title, book)
    text = book[beginning:ending].decode('ascii', 'ignore')
    tokenizer = nltk.data.load('nltk/english.pickle')
    return tokenizer.tokenize(text)
