#!/usr/bin/python3


def getIntBE(b):
	return b[3] | (b[2] << 8) | (b[1] << 16) | (b[0] << 24)	

def readChapters(a):
	a = a[8:]
	n = int(a[0])
	a = a[1:]
	while n > 0:
		a = a[8:]
		l = int(a[0])
		a = a[1:]
		t = a[:l]
		a = a[l:]
		print('chapter: ' + str(t))
		n = n - 1

def readMeta(f,pos,end):
	if pos+8 < end:
		f.seek(pos+4) # skips always 0 byte
		bytesRead = f.read(4)
		atomSize = getIntBE(bytesRead)
		pos = f.seek(pos+8+atomSize+4) #skips hdlr atom
		while pos < end:
			pos = f.seek(pos+4)
			bytesRead = f.read(4)
			print('tag: ' + str(bytesRead))
			bytesRead = f.read(4)
			dataSize = getIntBE(bytesRead)
			f.seek(pos+20)
			bytesRead = f.read(dataSize-16)
			pos = f.tell()
			print('value: %s' % bytesRead.decode('utf-8'))


def readAtoms(f,pos,end):
	if pos < end:
		f.seek(pos)
		bytesRead = f.read(4)
		nRead = len(bytesRead)
		pos = pos + nRead
		while nRead > 0:
			atomSize = getIntBE(bytesRead)
			if atomSize < 1:
				break
			bytesRead = f.read(4)
			nRead = len(bytesRead)
			pos = pos + nRead
			atomName = bytesRead.decode('utf-8')
			print('atom name: %s' % atomName)
			if atomName in ['moov','udta']:
				readAtoms(f, pos, pos+atomSize-8)
			elif atomName == 'meta':
				readMeta(f,pos,pos+atomSize-8)
			elif atomName == 'chpl':
				readChapters(f.read(atomSize-8))
			pos = f.seek(pos+atomSize-8)
			bytesRead = f.read(4)
			nRead = len(bytesRead)
			pos = pos + nRead

with open('./h.mp4', 'rb') as f:
	end = f.seek(0, 2)
	readAtoms(f, 0, end)

