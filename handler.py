import sys
import os

cwd = os.path.dirname(os.path.realpath(__file__))
site_pkgs = os.path.join(cwd, "venv", "lib", "python2.7", "site-packages")
sys.path.append(site_pkgs)

from book_tweet import book_tweet

def __main():
    sentence = book_tweet.main()

    response = {
        'statusCode': 200,
        'body': sentence
    }
    return response;

def main(event, context):
    __main();

if __name__ == "__main__":
    print(__main())
