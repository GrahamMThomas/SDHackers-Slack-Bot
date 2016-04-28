def main():
	try:
		magicalFile = open('Txts/magical.txt', 'r')
		magicalFile.readline()
		token = magicalFile.readline()
		print token
		magicalFile.close()
	except Exception, e:
		print "ERROR: magical.txt not found... You must populate this manually"
		open('Txts/magical.txt', 'w')

if __name__ == '__main__':
	main()