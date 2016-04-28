#PURPOSE:	Find the next line in a text file
#			and print it to Node.js
def main():
	#Directories Containing Txt Files
	
	lastLineFile = "Txts/last_line_insults.txt"
	insultsFile = "Txts/insults.txt"

	#Attempt to Open lastLineFile, get the integer
	#	close, then add one to it.
	try:
		llf = open(lastLineFile, 'r')
		startfrom = int(llf.read())
		llf.close()
		llf = open(lastLineFile, 'w')
		print >> llf, startfrom + 1
	except:
		print "ERROR: last_line.txt not found... creating"
		open(lastLineFile, 'w')

	#Try to open insultsFile
	try:
		f = open(insultsFile, 'r')
	except:
		open(insultsFile, 'w')

	#Go to the line from lastLineFile
	#	and the line from insultsFile
	i = 0
	try:
		for line in f.readlines():		
			if(i == startfrom):
				print line
				break
			i+=1
	#If no lines availiable...
	except:
		print "No messages availiable, please wait..."
	print "No messages availiable, it's broken..."

if __name__ == '__main__':
	main()