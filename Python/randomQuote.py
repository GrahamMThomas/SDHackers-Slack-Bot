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

randomFile = "Txts/random.txt"
magicalNumbers = "Txts/magicalNumbers.txt"
random.seed(datetime.datetime.now())

#	This function splits up all the quotes
#	in random.txt and then randomly chooses
#	one of them to print
def getQuote():
	
	try:
		f = open(randomFile, 'r')
	except:
		print 'ERROR: interesting.txt not found'	

	quotes = f.read()
	quotes = quotes.split('\n')

	try:
		num = random.randint(0, len(quotes)-2)
		print quotes[num]
	except:
		print "Sorry I failed... Couldn't find anything... Please try again"

	f.close()


#	This function pulls a 'magic number' out to
#	determine which archive page to use. Then
#	goes to that page and parse the titles. It then
#	randomly chooses one title to place into 
#	random.txt
def parseQuote():

	begin = "Did you know... "
	begin2 = "Food for thought... "

	# Grab number from magicalNumbers.txt
	try:
		f = open(magicalNumbers, 'r')
		magicNumbers = []
	        magicNumbers = f.read()
        	magicNumbers.split('\n')
		randNum = magicNumbers[random.randint(0, len(magicNumbers))]
		f.close()

	except:
		print 'Error... Could not open magicalNumber.txt...'

	# Create link and parse for TIL
	try:
		link = 'https://web.archive.org/web/' + randNum + '/https://www.reddit.com/r/todayilearned/'
		page = requests.get(link)
		tree = html.fromstring(page.content)
        	title = tree.xpath('//div[@class="entry unvoted"]/p[@class="title"]/a/text()')
	except:
		pass

        try:
                f = open(randomFile, 'a')
        except:
                print "Error... InterestingFile won't open..."

	# Format and print
        try:
                arranged = str(title).split('\',')
                word = arranged[random.randint(2, len(arranged))]
                word2 = word.split('",')
                if (len(word2) > 1):
                        formatWord = word2[0][2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = formatWord[4:]
			formatWord = begin + formatWord
                        f.write(formatWord + "\n")
                else:
                        formatWord = word[2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = formatWord[4:]
			formatWord = begin + formatWord
                        f.write(formatWord + "\n")

        except:
                pass

	# Create link for showerthoughts
	try:
		link = 'https://web.archive.org/web/' + randNum + '/https://www.reddit.com/r/Showerthoughts/'
	        page = requests.get(link)
        	tree = html.fromstring(page.content)
        	title = tree.xpath('//div[@class="entry unvoted"]/p[@class="title"]/a/text()')
	except:
		pass

	# Format
        try:
                arranged = str(title).split('\',')
                word = arranged[random.randint(2, len(arranged))]
                word2 = word.split('",')
                if (len(word2) > 1):
                        formatWord = word2[0][2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = begin2 + formatWord
                        f.write(formatWord + "\n")
                else:
                        formatWord = word[2:]
                        formatWord = formatWord.translate(None, "\\[]")
			formatWord = begin2 + formatWord
                        f.write(formatWord + "\n")

        except:
                pass


	f.close()


#	Main function runs parseQuote() couple times in case
#	the link does not work
def main():
	f = open(randomFile, 'w').close()
	
	for num in range(0, 2):
		parseQuote()
	getQuote()

if __name__ == '__main__':
	main()
