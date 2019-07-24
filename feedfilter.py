import feedparser
import re 
import classifier
def read(feed,classifier):
    f = feedparser.parse(feed)
    for entry in f['entries']:
        print('------------------')
        print('Titile: '+entry['title'])
        print('Publisher: '+entry['publishier'])
        print('Summary: '+entry['summary'])
        fulltext="%s\n%s\n%s" % (entry['title'],entry['publisher'],entry['summary'])
        print('Guess'+str(classifier.classify(fulltext)))
        cl = input('Enter category: ')
        classifier.train(fulltext,cl)