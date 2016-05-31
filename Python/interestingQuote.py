#	05/24/2016
#	DESCRIPTION: This script goes through the archives
#			of the subreddit TIL and showerthoughts
#			then pull one of the post into a file
#			named random.txt. It will grab several
#			quotes in case a quote could not be grabbed.
#			Then it prints out a random quote form
#			random.txt.

import random
import datetime
import requests
from lxml import html
randNum = ['20160401142806', '20160404010627', '20160405091410',
	'20160407121822', '20160408213640', '20160409141021',
	'20160410222259', '20160410222259', '20160412054747',
	'20160414000246', '20160415003316', '20160416000815',
	'20151208151736', '20151209170059', '20151211034408',
	'20151212161957', '20151125231114', '20151126033027',
	'20151127032024', '20150616160811', '20150617000513',
	'20150618014231', '20150619160045', '20150215230956',
	'20150216004131']

magicLink = random.randint(0,24)
magicQuote = random.randint(0,18)

#	Function finds a random archive of a
#	TIL subreddit page and post one of its
#	titles
def parseQuote1():

	begin = "Did you know... "

	# Create link and parse for TIL
	try:
		link = 'https://web.archive.org/web/' + randNum[magicLink] + '/https://www.reddit.com/r/todayilearned/'
		page = requests.get(link)
		tree = html.fromstring(page.content)
        	title = tree.xpath('//div[@class="entry unvoted"]/p[@class="title"]/a/text()')
	except:
		pass

	# Format and print
        try:
                arranged = str(title).split('\',')
		word = arranged[magicQuote]
                word2 = word.split('",')
                if (len(word2) > 1):
                        formatWord = word2[0][2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = formatWord[4:]
			formatWord = begin + formatWord
			print formatWord
                else:
                        formatWord = word[2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = formatWord[4:]
			formatWord = begin + formatWord
			print formatWord

        except:
                pass

#	Function finds a quote from the showerthought
#	subreddit and posts a title from it
def parseQuote2():

	begin2 = "Food for thought... "

	#Create link for showerthoughts
        try:
                link = 'https://web.archive.org/web/' + randNum[magicLink] + '/https://www.reddit.com/r/Showerthoughts/'
                page = requests.get(link)
                tree = html.fromstring(page.content)
                title = tree.xpath('//div[@class="entry unvoted"]/p[@class="title"]/a/text()')

        	# Format and print
                arranged = str(title).split('\',')
		word = arranged[magicQuote]
                word2 = word.split('",')
                if (len(word2) > 1):
                        formatWord = word2[0][2:]
                        formatWord = formatWord.translate(None, "\\[]")
                        formatWord = begin2 + formatWord
                        print formatWord
                else:
                        formatWord = word[2:]
                        formatWord = formatWord.translate(None, "\\[]")
                        formatWord = begin2 + formatWord
                        print formatWord

        except:
                pass


def main():
	
	decision = random.randint(0, 1)
	if decision == 0:
		parseQuote1()
	else:
		parseQuote2()
	print 'I have failed you... Tell @vinhvu100 how much his code sucks'

if __name__ == '__main__':
	main()
