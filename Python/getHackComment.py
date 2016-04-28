import urllib
import os
import time
import sys

numLines = 0
startfrom = 0
magicalLink = ''

def lookForComment(f):
	#Open URL and strip html
	response = urllib.urlopen(magicalLink)
	html = response.read()

	#Try to parse html and get the comment.
	try:
		html = html[html.index('commentMessage')+16:html.index('<div class="actionButtonsBlock">')]	
		html = html.replace("&quot;", "\"")
		html = html[:html.index("<img src")]
	except:
		pass

	#Delete surrounding white space.
	html = html.strip()	

	#[[commentMessage]] means there are no comments, and some links 
	#	redirect oddly causing huge strings.
	if  not (html == "[[commentMessage]]" or html == "" or len(html) > 500):
		print >> f, html
		global numLines
		numLines += 1

def main():
	global numLines
	global startfrom
	global magicalLink	

	magicFileUrl = "Txts/magical.txt"
	lastLineFile = "Txts/last_line_comments.txt"
	commentsFile = "Txts/comments.txt"

	try:
			magicalFile = open(magicFileUrl, 'r')
			magicalLink	= magicalFile.readline()
			magicalFile.close()
	except:
		print "ERROR: magical.txt not found... You must populate this manually"
		open("magical.txt", 'w')

	#Continue running...
	while(True):

		#Attempt to get startfrom variable from 
		#	the lastLineFile. Create the file if
		#	it does not exist
		try:
			llf = open(lastLineFile, 'r')
			startfrom = int(llf.read())
			llf.close()
		except:
			print "ERROR: last_line.txt not found... creating"
			open(lastLineFile, 'w')

		#if there are less than 50 comments cached...
		if startfrom + 50 > numLines:

			#Retrieve the amount of lines in the commentsFile
			numLines = sum(1 for line in open(commentsFile))

			f = open(commentsFile, 'a')

			#While there are less than 50 cached...
			while(startfrom	+ 50 > numLines):
				print ("%d of %d comments") % (startfrom,numLines)
				lookForComment(f)

		#Sleep for 10 seconds.
		else:
			time.sleep(10)


if __name__ == '__main__':
	main()