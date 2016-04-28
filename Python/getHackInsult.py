import urllib
import os
import time
import sys

numLines = 0
startfrom = 0

def lookForInsult(f):
	#Open url and scrape html
	response = urllib.urlopen('http://www.insultgenerator.org/')
	html = response.read()

	#Attempt to parse html, leaving only the insult
	try:
		html = html[html.index('<div class="wrap">')+28:html.index('<center>')-7]	
		html = html.replace("&quot;", "\"")
	except:
		pass

	#Strip white space off the sides.
	html = html.strip()	

	#if the insult was successfully parsed...
	if  not (html == ""):
		print html
		print >> f, html
		global numLines
		numLines += 1

def main():
	global numLines
	global startfrom

	lastLineFile = "Txts/last_line_insults.txt"
	insultsFile = "Txts/insults.txt"

	#Continue running...
	while(True):

		#Open lastLineFile and save startfrom.
		try:
			llf = open(lastLineFile, 'r')
			startfrom = int(llf.read())
			llf.close()
		#Create if doesn't exist.
		except:
			print "ERROR: last_line_insults.txt not found... creating"
			llfw = open(lastLineFile, 'w')
			print >> "0", llfw
			llfw.close()

		#If there are less that 50 new insults cached...
		if startfrom + 50 > numLines:
			f = ''

			#Get number of lines in the the insultsFile
			numLines = sum(1 for line in open(insultsFile))

			f = open(insultsFile, 'a')

			#While there are less than 50 insults cached...
			while(startfrom	+ 50 > numLines):
				print ("%d of %d insults") % (startfrom,numLines)
				try:
					lookForInsult(f)
			  	except:
			  		pass
			  		
		#Sleep for 10 seconds
		else:
			time.sleep(10)


if __name__ == '__main__':
	main()