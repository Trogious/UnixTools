#!/usr/local/bin/python3.3

import sys
import os

def usage():
	print('Syntax: ' + sys.argv[0] + ' [-h] <torrent_file>')
	sys.exit(1)

argsLen = len(sys.argv)
if argsLen < 2:
	usage()

humanReadableSize = False

if sys.argv[1].strip() == '-h':
	if argsLen < 3:
		usage()
	else:
		file = sys.argv[2]
		humanReadableSize = True
else:
	file = sys.argv[1]

if not (file.endswith('.torrent') and os.path.exists(file) and os.path.isfile(file)):
	usage()

def getHumanReadable(size):
	units = ['B','K','M','G','T','P','E']
	i = 0
	prevSize = 0
	while size > 1023:
		prevSize = float(size)
		size >>= 10
		i += 1
	if i > 0:
		size = round(prevSize/1024,2)
	return str(size) + ' ' + units[i]

import codecs

maxBuf = 1024
found = False
infoFound = False
buf = ''
size = 0

with codecs.open(file, 'r', 'iso8859-1') as f:
	while not found:
		newBuf = f.read(maxBuf)
		buf = buf + newBuf
		if not infoFound:
			infoIdx = buf.find(':info')
			if infoIdx >=0:
				infoFound = True
				buf = buf[infoIdx+5:]
			else:
				buf = buf[len(buf)-6:]
		else:
			while True:
				lenStartIdx = buf.find('d6:lengthi')
				nameIdx = buf.find('4:name')
				sizeFound = False
				if lenStartIdx >= 0:
					lenEndIdx = buf.find('e',lenStartIdx+10)
					if lenEndIdx >= 0:
						size = size + int(buf[lenStartIdx+10:lenEndIdx])
						buf = buf[lenEndIdx+1:]
						sizeFound = True
					else:
						buf = buf[lenStartIdx:]
				if not sizeFound and nameIdx >= 0:
					buf = buf[nameIdx:]
					nameLenIdx = buf.find(':',2)
					if nameLenIdx >= 0:
						nameLenStr = buf[6:nameLenIdx]
						nameLenSize = len(nameLenStr)
						nameLen = int(nameLenStr)
						if len(buf) >= nameLen+nameLenSize+7:
							name = buf[nameLenSize+7:nameLen+nameLenSize+7]
							found = True
				if not sizeFound:
					break
		if newBuf == '':
			break

if found:
	if humanReadableSize:
		print(name + ' ' + getHumanReadable(size))
	else:
		print(name + ' ' + str(size) + ' B')
else:
	print('Total (probable) size in bytes: ' + str(size))


